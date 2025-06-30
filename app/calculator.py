import sys
import re
from app.calculation import CalculationFactory
from app.logger import get_logger
from app.memento import CalculationMemento, CalculationHistory
from app.history import display_history, save_history, new_history, delete_calculation, load_history
from app.exceptions import OperationError, CalculatorError, HistoryError
from app.config import HISTORY_FILE_PATH

log = get_logger("calculator")
precedence = {"1": ['+', '-', '--'], "2": ['*', '/', '%', '/%', '//'], "3": ['^', '?']}

def get_precedence_group(operator):
    """Return the precedence group for a given operator."""
    for group, ops in precedence.items():
        if operator in ops:
            return group
    return None

def parse_ans_reference(token, history):
    """Parse 'ans' or 'ans(n)' and return the corresponding previous result."""
    try:
        if token == 'ans':
            return history.get_previous_result(len(history.get_history()))
        match = re.match(r'ans\((\d+)\)', token)
        if match:
            n = int(match.group(1))
            return history.get_previous_result(n)
        raise CalculatorError(f"Invalid ans reference: {token}")
    except HistoryError as e:
        log.error(f"Failed to parse ans reference: {str(e)}")
        raise
    except Exception as e:
        log.error(f"Failed to parse ans reference: {str(e)}")
        raise CalculatorError(f"Invalid ans reference: {str(e)}")

def format_ans_token(token, value=None):
    """Format ans(n) token with its resolved value in parentheses."""
    if value is not None and token.startswith('ans'):
        return f"{token} ({value})"
    return token

def calculate_expression(input_str, history):
    """Process a calculation input and perform operations using CalculationFactory."""
    try:
        log.debug(f"User entered input: {input_str}")
        u_input_lst = input_str.strip().split()
        
        if len(u_input_lst) < 3 or len(u_input_lst) % 2 == 0:
            log.error("Invalid format: Expected 'number operator number [operator number]...'")
            raise CalculatorError("Invalid format: Expected 'number operator number [operator number]...'")
        
        values = u_input_lst.copy()
        try:
            first_token = values.pop(0)
            if first_token.startswith('ans'):
                result = parse_ans_reference(first_token, history)
                formatted_first_token = format_ans_token(first_token, result)
            else:
                result = float(first_token)
                formatted_first_token = first_token
            log.debug(f"Initial result: {result}")
        except ValueError as e:
            log.error(f"Invalid format: First value must be a number or ans(n), input {input_str}")
            raise CalculatorError("Invalid command: Input must start with a number or ans(n)")
        
        precedence_group = None
        steps = []
        original_input = [first_token]  # Store original tokens, not formatted
        formatted_input = [formatted_first_token] + values  # Formatted for memento
        while values:
            if len(values) < 2:
                log.error("Incomplete expression: Expected operator and number")
                raise CalculatorError("Incomplete expression: Expected operator and number")
            
            operator = values.pop(0)
            original_input.append(operator)
            formatted_input.append(operator)
            current_group = get_precedence_group(operator)
            if current_group is None:
                log.warning(f"Unsupported operator detected: {operator}")
                raise OperationError(f"Unsupported operator {operator}. Only {', '.join(sum(precedence.values(), []))} allowed")
            
            if precedence_group is None:
                precedence_group = current_group
                log.debug(f"Set precedence group to {precedence_group}")
            elif current_group != precedence_group:
                log.warning(f"Mixed operator precedence detected: {operator} (group {current_group}) with group {precedence_group}")
                raise OperationError(f"Mixed operator precedence not allowed: Cannot use {operator} (group {current_group}) with group {precedence_group} operators")
            
            try:
                next_token = values.pop(0)
                original_input.append(next_token)
                if next_token.startswith('ans'):
                    num = parse_ans_reference(next_token, history)
                    formatted_next_token = format_ans_token(next_token, num)
                else:
                    num = float(next_token)
                    formatted_next_token = next_token
                formatted_input.append(formatted_next_token)
                log.debug(f"Processing {operator} {num}")
            except ValueError as e:
                log.error(f"Expected a number or ans(n) after operator: {str(e)}")
                raise CalculatorError(f"Expected a number or ans(n) after operator")
            
            try:
                calculation = CalculationFactory.create_calculation(operator, result, num)
                new_result = calculation.execute()
                log.debug(f"Current result: {new_result}")
                step_input = f"{formatted_input[0]} {operator} {formatted_next_token}"
                formatted_input = [str(new_result)] + values
                original_input = [str(new_result)] + values
                memento = CalculationMemento(step_input, operator, result, num, new_result)
                steps.append(memento)
                result = new_result
            except ValueError as ve:
                log.error(f"Calculation error: {str(ve)}")
                raise OperationError(f"Calculation error: {str(ve)}")
        
        history.save_calculation_group(input_str, result, steps)
        log.info(f"Final calculation result: {result}")
        return result
    
    except (OperationError, CalculatorError, HistoryError) as e:
        log.warning(f"Invalid input: {str(e)}")
        raise

def calculator(history=None):
    """Main calculator function."""
    if history is None:
        history = CalculationHistory(HISTORY_FILE_PATH)
    print("Welcome to Dom Urso's Calculator!")
    print("Enter calculations like '1 + 2 + 3' or 'ans(1) + 2', 'history' to view past calculations, or 'exit' to quit.")
    while True:
        try:
            u_input = input(">> ").strip().lower()
            if not u_input:
                print("Please enter a calculation, 'history', 'save', 'new', 'delete <index>', 'load <filename>', or 'exit'")
                continue
            
            if u_input == 'exit':
                log.info("Exiting calculator")
                print("Exiting the Calculator")
                sys.exit(0)
            
            if u_input == 'help':
                print(f'''
                    Welcome To Dom Urso's Calculator
                    Enter calculations in the format: number operator number [operator number]...
                    Numbers can be numeric values or 'ans(n)' (e.g., 'ans(1)' for the first calculation, 'ans(2)' for the second, etc.)
                    'ans' alone refers to the most recent calculation.
                    In history, ans(n) will show its resolved value in parentheses, e.g., 'ans(1) (6.0) * 2'
                    Supported Operators:
                      + (addition), - (subtraction), -- (absolute difference)
                      * (multiplication), / (division), % (modulo), /% (percentage), // (integer division)
                      ^ (power), ? (root)
                    Precedence Groups:
                      Group 1: +, -, --
                      Group 2: *, /, %, /%, //
                      Group 3: ^, ?
                    Commands:
                      help - display this help message
                      precedence - view operator precedence groupings
                      history - view past calculations with steps
                      save - save current history to a timestamped CSV file
                      new - start a new history (clears current history)
                      delete <index> - delete the calculation at the given index (e.g., 'delete 1')
                      load <filename> - load history from a backup CSV file (e.g., 'load history_20250630_182058.csv')
                      exit - exit the program
                    Examples:
                      1 + 2 - 3
                      ans(1) * 2
                      ans + 5
                      25 ? 2 (square root)
                      delete 1
                      load history_20250630_182058.csv
                ''')
                continue
            
            if u_input == 'precedence':
                print(f"Precedence groups define the order of operations:\n{precedence}")
                continue
            
            if u_input == 'history':
                display_history(history)
                continue
            
            if u_input == 'save':
                save_history(history)
                continue
            
            if u_input == 'new':
                new_history(history)
                continue
            
            if u_input.startswith('delete '):
                try:
                    index_str = u_input.split(' ', 1)[1].strip()
                    index = int(index_str)
                    delete_calculation(history, index)
                except ValueError as e:
                    print(f"Error: Invalid index format: {str(e)}")
                    print("Please use format: delete <index> (e.g., 'delete 1')")
                except HistoryError as e:
                    print(f"Error: {str(e)}")
                    print("Please use format: delete <index> (e.g., 'delete 1')")
                continue
            
            if u_input.startswith('load '):
                try:
                    filename = u_input.split(' ', 1)[1].strip()
                    load_history(history, filename)
                except HistoryError as e:
                    print(f"Error: {str(e)}")
                    print("Please use format: load <filename> (e.g., 'load history_20250630_182058.csv')")
                continue
            
            try:
                first_token = u_input.split()[0]
                if not (first_token.startswith('ans') or float(first_token)):
                    raise CalculatorError("Invalid command: Input must start with a number or ans(n)")
            except (ValueError, IndexError) as e:
                raise CalculatorError(f"Invalid command: Input must start with a number or ans(n)")
            
            result = calculate_expression(u_input, history)
            print(f"Result: {result}")
        
        except (OperationError, CalculatorError, HistoryError) as e:
            log.warning(f"Error: {str(e)}")
            print(f"Error: {str(e)}")
            print("Please try again or type 'help' for assistance")
            continue
        except Exception as e:
            log.warning(f"Unexpected error: {str(e)}")
            print(f"Unexpected error: {str(e)}")
            print("Please try again or type 'help' for assistance")
            continue
