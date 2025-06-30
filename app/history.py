from app.memento import CalculationHistory
from app.logger import get_logger
from app.exceptions import HistoryError
import os

logger = get_logger("history")

def display_history(history_obj):
    """Display the history of calculation groups."""
    try:
        calculations = history_obj.get_history()
        if calculations.empty:
            print("No calculations in history.")
            logger.info("Displayed empty calculation history")
            return
        print("\nCalculation History:")
        for i, group in calculations.iterrows():
            print(f"{i + 1}. {group['timestamp']}: {group['input']} = {group['result']}")
            for j, step in enumerate(group['steps'], 1):
                print(f"   Step {j}: {step['input']} = {step['result']}")
        logger.info(f"Displayed calculation history with {len(calculations)} groups")
    except Exception as e:
        logger.error(f"Failed to display history: {str(e)}")
        raise HistoryError(f"Failed to display history: {str(e)}")

def save_history(history_obj):
    """Save the current history to a timestamped backup file."""
    try:
        backup_file = history_obj.save_history_to_file()
        print(f"History saved to {backup_file}")
        logger.info(f"User saved history to {backup_file}")
    except HistoryError as e:
        logger.warn(f"Error saving history: {str(e)}")
        raise

def new_history(history_obj):
    """Clear the current history and start a new one."""
    try:
        history_obj.new_history()
        print("Started a new history. Current history cleared.")
        logger.info("User started a new history")
    except HistoryError as e:
        logger.warn(f"Error starting new history: {str(e)}")
        raise

def delete_calculation(history_obj, index):
    """Delete the calculation at the given index."""
    try:
        history_obj.delete_calculation(index)
        print(f"Deleted calculation {index}")
        logger.info(f"User deleted calculation {index}")
    except HistoryError as e:
        logger.warn(f"Error deleting calculation {index}: {str(e)}")
        raise

def load_history(history_obj, filename):
    """Load history from a specified backup file."""
    try:
        history_obj.load_history_from_file(filename)
        print(f"Loaded history from {filename}")
        logger.info(f"User loaded history from {filename}")
    except HistoryError as e:
        logger.warn(f"Error loading history from {filename}: {str(e)}")
        raise
