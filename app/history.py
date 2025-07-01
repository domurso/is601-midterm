from app.exceptions import HistoryError
from app.logger import get_logger
from app.config import HISTORY_BACKUP_DIR
from app.observer import Observer
from colorama import Fore, Style

logger = get_logger("history")

class HistoryDisplayObserver(Observer):
    def update(self, event, data):
        if event == "calculation_added":
            print(f"{Fore.GREEN}New calculation added: {data['input']} = {data['result']}{Style.RESET_ALL}")
            for idx, step in enumerate(data['steps'], 1):
                print(f"   Step {Fore.CYAN}{idx}{Style.RESET_ALL}: {step['input']} = {step['result']}")
        elif event == "history_saved":
            print(f"{Fore.GREEN}History saved to {Fore.CYAN}{data['backup_file']}{Style.RESET_ALL}")
        elif event == "history_cleared":
            print(f"{Fore.GREEN}Started new history{Style.RESET_ALL}")
        elif event == "calculation_deleted":
            print(f"{Fore.GREEN}Deleted calculation {Fore.CYAN}{data['index']}{Style.RESET_ALL}")
        elif event == "history_loaded":
            print(f"{Fore.GREEN}Loaded history from {Fore.CYAN}{data['filename']}{Style.RESET_ALL}")

def display_history(history):
    """Display the calculation history with colored output."""
    try:
        if history.get_history().empty:
            print(f"{Fore.RED}No calculations in history{Style.RESET_ALL}")
            return
        
        print(f"{Fore.YELLOW}Calculation History:{Style.RESET_ALL}")
        for idx, row in history.get_history().iterrows():
            print(f"{Fore.CYAN}{idx + 1}.{Style.RESET_ALL} {Fore.YELLOW}{row['timestamp']}{Style.RESET_ALL}: {Fore.GREEN}{row['input']}{Style.RESET_ALL} = {Fore.YELLOW}{row['result']}{Style.RESET_ALL}")
            for step_idx, step in enumerate(row['steps'], 1):
                print(f"   Step {Fore.CYAN}{step_idx}{Style.RESET_ALL}: {step['input']} = {Fore.YELLOW}{step['result']}{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"Failed to display history: {str(e)}")
        print(f"{Fore.RED}Failed to display history: {str(e)}{Style.RESET_ALL}")
        raise HistoryError(f"Failed to display history: {str(e)}")

def save_history(history):
    """Save the current history to a backup file with colored output."""
    try:
        backup_file = history.save_history_to_file()
        print(f"{Fore.GREEN}History saved to {Fore.CYAN}{backup_file}{Style.RESET_ALL}")
    except HistoryError as e:
        logger.error(f"Failed to save history: {str(e)}")
        print(f"{Fore.RED}Failed to save history: {str(e)}{Style.RESET_ALL}")
        raise

def new_history(history):
    """Start a new history, clearing the current one, with colored output."""
    try:
        history.new_history()
        print(f"{Fore.GREEN}Started new history{Style.RESET_ALL}")
    except HistoryError as e:
        logger.error(f"Failed to start new history: {str(e)}")
        print(f"{Fore.RED}Failed to start new history: {str(e)}{Style.RESET_ALL}")
        raise

def delete_calculation(history, index):
    """Delete a calculation from history by index with colored output."""
    try:
        history.delete_calculation(index)
        print(f"{Fore.GREEN}Deleted calculation {Fore.CYAN}{index}{Style.RESET_ALL}")
    except HistoryError as e:
        logger.error(f"Failed to delete calculation {index}: {str(e)}")
        print(f"{Fore.RED}Failed to delete calculation {Fore.CYAN}{index}{Style.RESET_ALL}: {str(e)}")
        raise

def load_history(history, filename):
    """Load history from a backup file with colored output."""
    try:
        history.load_history_from_file(filename)
        print(f"{Fore.GREEN}Loaded history from {Fore.CYAN}{filename}{Style.RESET_ALL}")
    except HistoryError as e:
        logger.error(f"Failed to load history from {filename}: {str(e)}")
        print(f"{Fore.RED}Failed to load history from {Fore.CYAN}{filename}{Style.RESET_ALL}: {str(e)}")
        raise
