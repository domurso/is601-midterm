"""
This is calculator.py it will contain the neccessities for the calculator to run
find other calcuator addition in the same directory
"""
import sys
from app.calculation import Calculation, CalculationFactory


precedence = {"1":['+','-'], "2":['*','/','%'], "3":['^', '?']}

def get_precedence_group(operator):
    for group,ops in precedence.items():
        if operator in ops:
            return group
    return None


def calculate_expression(input_str):
    #print(input_str)
    try:
                #print(input_str)
                u_input_lst = input_str.split()
                #print(u_input_lst)
                if len(u_input_lst) < 3 or len(u_input_lst) % 2 == 0:
                    print("Invalid Format: Expected following example '1 + 1 + 2'")
                    raise ValueError("Invalid format")
                values = u_input_lst.copy()
                #print("step2")
                try:
                    result = float(values.pop(0))
                    #print(f"result= {result}")
                except ValueError:
                    print("First Value must be a number")
                    raise ValueError("Invalid Format")
                #print("step3",values)
                precedence_group = None
                while values:
                    #print("step4")
                    if len(values) < 2:
                        print("Incomplete expression: Expected operator and number")

                    operator = values.pop(0)
                    current_group = get_precedence_group(operator)
                    #print(f"op={operator}")
                    if current_group is None:
                        print(f"Unsupported operator {operator} only {precedence} allowed")
                    
                    if precedence_group is None:
                        precedence_group = current_group
                    elif current_group != precedence_group:
                        raise ValueError(f"Mixed operator precedence not allowed: cannot use {operator} (group {current_group}) with group {precedence_group} operators, {precedence}")

                    try:
                        num = float(values.pop(0))
                    except ValueError:
                        print("Expected a number after operator")

                    try:
                        #print(operator,result,num)
                        calculation = CalculationFactory.create_calculation(operator,result,num)
                        #print("xxxxx")
                        #print(calculation)
                        
                    except ValueError as ve:
                        print("Calculation Error")
                        raise ValueError(ve, "Invalid argument passed")
                        break

                    try:
                        result = calculation.execute()

                    except Exception as e:
                        print(e)
                        print("invalid argument passed")
                        break

                return result
    except ValueError as e:
            print("invalid input: {str(e)}")
            return e


def calculator() -> None: # Calculator
    print("Welcome to my Calculator, as of right now it doesnt do anything, type 'exit' to exit :) ")
    while True:
        try:
            u_input: str = input(">> ").strip().lower()
            if not u_input: #if the user enters nothing then ask again
                print("Please 'exit' to exit")
                continue
            
            # User Commands
            if u_input == 'exit': # to exit the program
                print("Exiting the Calculator")
                sys.exit(0)

            elif u_input == 'help': # Help Command
                print(f'''
                      Welcome To Dom Urso's Calculator
                      The Current Available Function Is Just a Calculator
                      Current Available Operations
                      "+" plus
                      "-" minus
                      "/" divide
                      "*" multiply
                      "%" modulo
                      "^" power
                      "?" root

                      Available Commands
                      help - to get help
                      exit - to exit the program
                      precedence - to view operation precedence groupings


                      Examples
                      Enter -> 1 + 1
                      Operations can be combined if they have the same precedence
                      ex + and - or *, /, and %
                      ''')
                continue
            elif u_input == 'precedence':
                print(f'Precidence is how operations are handled in math, people most commonly use pemdas but there are other operations aswell, these are the following grouping for precidence in my program\n {precedence}')
                continue
            
            try:
                float(u_input[0])
            except:
                raise ValueError("Invalid Command Entered")
            try:
                #print(u_input)
                result = calculate_expression(u_input)
                print(f"Result: {result}")
            except:
                raise ValueError("Issue Handling Expression, Please try again")
        

        except Exception as e:
            print("\n\n",e)
            continue
