"""
This is calculator.py it will contain the neccessities for the calculator to run
find other calcuator addition in the same directory
"""
import sys

def calculator() -> None: # Calculator
    print("Welcome to my Calculator, as of right now it doesnt do anything, type 'exit' to exit :) ")
    while True:
        try:
            u_input: str = input(">> ").strip().lower()
            if not u_input: #if the user enters nothing then ask again
                print("Please 'exit' to exit")
                continue
        
            if u_input == 'exit': # to exit the program
                print("Exiting the Calculator")
                sys.exit(0)
        except Exception as e:
            print("\n\n",e)
