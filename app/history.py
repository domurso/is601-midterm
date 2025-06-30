from app.memento import CalculationHistory
from app.logger import get_logger
from app.exceptions import HistoryError
import os
from colorama import Fore, Style
logger = get_logger("history")

def display_history(history_obj):
    try:
        calculations = history_obj.get_history()
        if calculations.empty:
            print(f"{Fore.RED}No calculations in history.{Style.RESET_ALL}")
            logger.info("Displayed empty calculation history")
            return
        print("\nCalculation History:")
        for i, group in calculations.iterrows():
            print(f"{i + 1}. {group['timestamp']}: {group['input']} = {group['result']}")
            for j, step in enumerate(group['steps'], 1):
                print(f"   Step {Fore.CYAN}{j}{Style.RESET_ALL}: {step['input']} = {Fore.YELLOW}{step['result']}{Style.RESET_ALL}")
        logger.info(f"Displayed calculation history with {len(calculations)} groups")
    except Exception as e:
        logger.error(f"Failed to display history: {str(e)}")
        raise HistoryError(f"Failed to display history: {str(e)}")

def save_history(history_obj):
    try:
        backup_file = history_obj.save_history_to_file()
        print(f"{Fore.GREEN}History saved to {backup_file}{Style.RESET_ALL}")
        logger.info(f"User saved history to {backup_file}")
    except HistoryError as e:
        logger.warning(f"Error saving history: {str(e)}")
        raise

def new_history(history_obj):
    try:
        history_obj.new_history()
        print(f"{Fore.ORANGE}Started a new history. Current history cleared.{Style.RESET_ALL}")
        logger.info("User started a new history")
    except HistoryError as e:
        logger.warning(f"Error starting new history: {str(e)}")
        raise

def delete_calculation(history_obj, index):
    try:
        history_obj.delete_calculation(index)
        print(f"{Fore.RED}Deleted calculation {index}{Style.RESET_ALL}")
        logger.info(f"User deleted calculation {index}")
    except HistoryError as e:
        logger.warning(f"Error deleting calculation {index}: {str(e)}")
        raise

def load_history(history_obj, filename):
    try:
        history_obj.load_history_from_file(filename)
        print(f"{Fore.Blue}Loaded history from {filename}{Style.RESET_ALL}")
        logger.info(f"User loaded history from {filename}")
    except HistoryError as e:
        logger.warning(f"Error loading history from {filename}: {str(e)}")
        raise
