import sys
import re
from app.calculation import CalculationFactory
from app.logger import get_logger
from app.memento import CalculationMemento, CalculationHistory
from app.history import display_history, save_history, new_history, delete_calculation, load_history
from app.exceptions import OperationError, CalculatorError, HistoryError
import os

log = get_logger("calculator")
precedence = {"1": ['+', '-', '--'], "2": ['*', '/', '%', '/%', '//'], "3": ['^', '?']}

# Initialize calculation history
history_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'calculation_history.csv')
history = CalculationHistory(history_file)

def get_precedence_group(operator):
    """Return the precedence group for a given operator."""
    for group, ops in precedence.items():
        if operator in ops:
            return group
    return None

def parse_ans_reference(token):
    """Parse 'ans' or 'ans(n)' and return the corresponding previous result."""
    try:
        if token == 'ans':
            return history.get_previous_result(len(history.get_history()))  # Most recent
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

def format_ans_token(token):
    """Format ans(n) token with its resolved value in parentheses."""
    try:
        if token.startswith('ans'):
            value = parse_ans_reference(token)
            return f"{token} ({value})"
        return token
    except (CalculatorError, HistoryError) as e:
        log.warn(f"Cannot format ans token {token}: {str(e)}")
        return token

def calculate_expression(input_str):
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
                result = parse_ans_reference(first_token)
            else:
                result = float(first_token)
            log.debug(f"Initial result: {result}")
        except ValueError as e:
            log.error(f"Invalid format: First value must be a number or ans(n), input {input_str}")
            raise CalculatorError(f"Invalid format: First value must be a number or ans(n): {str(e)}")
        
        precedence_group = None
        steps = []  # Collect mementos for each operation step
        original_input = [first_token] + values  # Preserve original input for history
        while values:
            if len(values) < 2:
                log.error("Incomplete expression: Expected operator and number")
                raise CalculatorError("Incomplete expression: Expected operator and number")
            
            operator = values.pop(0)
            current_group = get_precedence_group(operator)
            if current_group is None:
                log.warn(f"Unsupported operator detected: {operator}")
                raise OperationError(f"Unsupported operator {operator}. Only {', '.join(sum(precedence.values(), []))} allowed")
            
            if precedence_group is None:
                precedence_group = current_group
                log.debug(f"Set precedence group to {precedence_group}")
            elif current_group != precedence_group:
                log.warn(f"Mixed operator precedence detected: {operator} (group {current_group}) with group {precedence_group}")
                raise OperationError(f"Mixed operator precedence not allowed: Cannot use {operator} (group {current_group}) with group {precedence_group} operators")
            
            try:
                next_token = values.pop(0)
                if next_token.startswith('ans'):
                    num = parse_ans_reference(next_token)
                else:
                    num = float(next_token)
                log.debug(f"Processing {operator} {num}")
            except ValueError as e:
                log.error(f"Expected a number or ans(n) after operator: {str(e)}")
                raise CalculatorError(f"Expected a number or ans(n) after operator: {str(e)}")
            
            try:
                calculation = CalculationFactory.create_calculation(operator, result, num)
                new_result = calculation.execute()
                log.debug(f"Current result: {new_result}")
                # Save operation step with formatted ans tokens
                step_input = f"{format_ans_token(original_input[0])} {operator} {format_ans_token(next_token)}"
                original_input = [str(new_result)] + values  # Update for next step
                memento = CalculationMemento(step_input, operator, result, num, new_result)
                steps.append(memento)
                result = new_result
            except ValueError as ve:
                log.error(f"Calculation error: {str(ve)}")
                raise OperationError(f"Calculation error: {str(ve)}")
        
        # Save the entire expression group with original input
        history.save_calculation_group(input_str, result, steps)
        log.info(f"Final calculation result: {result}")
        return result
    
    except (OperationError, CalculatorError, HistoryError) as e:
        log.warn(f"Invalid input: {str(e)}")
        print(f"Invalid input: {str(e)}")
        print("Please use format: number operator number [operator number]..., where number can be a number or ans(n)")
        print(f"Supported operators: {', '.join(sum(precedence.values(), []))}")
        print("Precedence groups: +,-,-- (group 1); *,/,%/%,// (group 2); ^,? (group 3)")
        print("Examples: '1 + 2 - 3', 'ans(1) * 2', 'ans + 5', '25 ? 2' (square root)")
        return None

def calculator():
    """Main calculator function."""
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
                      load <filename> - load history from a backup CSV file (e.g., 'load history_20250630_165456.csv')
                      exit - exit the program
                    Examples:
                      1 + 2 - 3
                      ans(1) * 2
                      ans + 5
                      25 ? 2 (square root)
                      delete 1
                      load history_20250630_165456.csv
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
                    print("Please use format: load <filename> (e.g., 'load history_20250630_165456.csv')")
                continue
            
            try:
                first_token = u_input.split()[0]
                if not (first_token.startswith('ans') or float(first_token)):
                    raise CalculatorError("Invalid command: Input must start with a number or ans(n)")
            except ValueError as e:
                raise CalculatorError(f"Invalid command: Input must start with a number or ans(n): {str(e)}")
            
            result = calculate_expression(u_input)
            if result is not None:
                print(f"Result: {result}")
        
        except (OperationError, CalculatorError, HistoryError) as e:
            log.warn(f"Error: {str(e)}")
            print(f"Error: {str(e)}")
            print("Please try again or type 'help' for assistance")
            continue
        except Exception as e:
            log.warn(f"Unexpected error: {str(e)}")
            print(f"Unexpected error: {str(e)}")
            print("Please try again or type 'help' for assistance")
            continue
