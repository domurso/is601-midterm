import sys
from app.calculation import CalculationFactory
from app.logger import get_logger
from app.memento import CalculationMemento, CalculationHistory
import os

log = get_logger("calculator")
precedence = {"1": ['+', '-', '--'], "2": ['*', '/', '%', '/%', '//'], "3": ['^', '?']}

# Initialize calculation history
history_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'calculation_history.json')
history = CalculationHistory(history_file)

def get_precedence_group(operator):
    """Return the precedence group for a given operator."""
    for group, ops in precedence.items():
        if operator in ops:
            return group
    return None

def calculate_expression(input_str):
    """Process a calculation input and perform operations using CalculationFactory."""
    try:
        log.debug(f"User entered input: {input_str}")
        u_input_lst = input_str.strip().split()
        
        if len(u_input_lst) < 3 or len(u_input_lst) % 2 == 0:
            log.error("Invalid format: Expected 'number operator number [operator number]...'")
            raise ValueError("Invalid format: Expected 'number operator number [operator number]...'")
        
        values = u_input_lst.copy()
        try:
            result = float(values.pop(0))
            log.debug(f"Initial result: {result}")
        except ValueError:
            log.error(f"Invalid format: First value must be a number, input {input_str}")
            raise ValueError("Invalid format: First value must be a number")
        
        precedence_group = None
        steps = []  # Collect mementos for each operation step
        while values:
            if len(values) < 2:
                log.error("Incomplete expression: Expected operator and number")
                raise ValueError("Incomplete expression: Expected operator and number")
            
            operator = values.pop(0)
            current_group = get_precedence_group(operator)
            if current_group is None:
                log.warn(f"Unsupported operator detected: {operator}")
                raise ValueError(f"Unsupported operator {operator}. Only {', '.join(sum(precedence.values(), []))} allowed")
            
            if precedence_group is None:
                precedence_group = current_group
                log.debug(f"Set precedence group to {precedence_group}")
            elif current_group != precedence_group:
                log.warn(f"Mixed operator precedence detected: {operator} (group {current_group}) with group {precedence_group}")
                raise ValueError(f"Mixed operator precedence not allowed: Cannot use {operator} (group {current_group}) with group {precedence_group} operators")
            
            try:
                num = float(values.pop(0))
                log.debug(f"Processing {operator} {num}")
            except ValueError:
                log.error("Expected a number after operator")
                raise ValueError("Expected a number after operator")
            
            try:
                calculation = CalculationFactory.create_calculation(operator, result, num)
                new_result = calculation.execute()
                log.debug(f"Current result: {new_result}")
                # Save operation step as a memento
                memento = CalculationMemento(f"{result} {operator} {num}", operator, result, num, new_result)
                steps.append(memento)
                result = new_result
            except ValueError as ve:
                log.error(f"Calculation error: {str(ve)}")
                raise ValueError(f"Calculation error: {str(ve)}")
        
        # Save the entire expression group
        history.save_calculation_group(input_str, result, steps)
        log.info(f"Final calculation result: {result}")
        return result
    
    except ValueError as e:
        log.warn(f"Invalid input: {str(e)}")
        print(f"Invalid input: {str(e)}")
        print("Please use format: number operator number [operator number]...")
        print(f"Supported operators: {', '.join(sum(precedence.values(), []))}")
        print("Precedence groups: +,-,-- (group 1); *,/,%/%,// (group 2); ^,? (group 3)")
        print("Examples: '1 + 2 - 3', '2 * 3 / 4', '16 ^ 2', '25 ? 2' (square root)")
        return None

def display_history():
    """Display the history of calculation groups."""
    calculations = history.get_history()
    if not calculations:
        print("No calculations in history.")
        log.info("Displayed empty calculation history")
        return
    print("\nCalculation History:")
    for i, group in enumerate(calculations, 1):
        print(f"{i}. {group['timestamp']}: {group['input']} = {group['result']}")
        for j, step in enumerate(group['steps'], 1):
            print(f"   Step {j}: {step['input']} = {step['result']}")
    log.info(f"Displayed calculation history with {len(calculations)} groups")

def calculator():
    """Main calculator function."""
    print("Welcome to Dom Urso's Calculator!")
    print("Enter calculations like '1 + 2 + 3', 'history' to view past calculations, or 'exit' to quit.")
    while True:
        try:
            u_input = input(">> ").strip().lower()
            if not u_input:
                print("Please enter a calculation, 'history', or 'exit'")
                continue
            
            if u_input == 'exit':
                log.info("Exiting calculator")
                print("Exiting the Calculator")
                sys.exit(0)
            
            if u_input == 'help':
                print(f'''
                    Welcome To Dom Urso's Calculator
                    Enter calculations in the format: number operator number [operator number]...
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
                      exit - exit the program
                    Examples:
                      1 + 2 - 3
                      2 * 3 / 4
                      16 ^ 2
                      25 ? 2 (square root)
                ''')
                continue
            
            if u_input == 'precedence':
                print(f"Precedence groups define the order of operations:\n{precedence}")
                continue
            
            if u_input == 'history':
                display_history()
                continue
            
            try:
                float(u_input.split()[0])
            except:
                raise ValueError("Invalid command: Input must start with a number")
            
            result = calculate_expression(u_input)
            if result is not None:
                print(f"Result: {result}")
        
        except Exception as e:
            log.warn(f"Error: {str(e)}")
            print(f"Error: {str(e)}")
            print("Please try again or type 'help' for assistance")
            continue
