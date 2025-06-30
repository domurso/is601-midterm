import json
import os
from datetime import datetime
from app.logger import get_logger

# Initialize logger for memento module
logger = get_logger("memento")

class CalculationMemento:
    """Memento class to store the state of a single operation step."""
    def __init__(self, input_str, operation, a, b, result):
        self._state = {
            'input': input_str,
            'operation': operation,
            'a': a,
            'b': b,
            'result': result
        }
    
    def get_state(self):
        """Return the stored state."""
        return self._state

class CalculationHistory:
    """Caretaker class to manage saving and retrieving calculation groups."""
    def __init__(self, history_file):
        self.history_file = history_file
        self.history = []
        # Ensure the directory for the history file exists
        history_dir = os.path.dirname(history_file)
        try:
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
                logger.info(f"Created history file directory: {history_dir}")
            self._load_history()
        except Exception as e:
            logger.error(f"Failed to initialize history file {history_file}: {str(e)}")
    
    def _load_history(self):
        """Load history from the JSON file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
                    logger.debug(f"Loaded history from {self.history_file}: {len(self.history)} entries")
            else:
                self.history = []
                logger.debug(f"No history file found at {self.history_file}; starting with empty history")
        except Exception as e:
            logger.error(f"Failed to load history from {self.history_file}: {str(e)}")
            self.history = []
    
    def save_calculation_group(self, input_str, result, steps):
        """Save a calculation group to the history file."""
        try:
            group = {
                'input': input_str,
                'result': result,
                'timestamp': datetime.now().isoformat(),
                'steps': [step.get_state() for step in steps]
            }
            self.history.append(group)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
            logger.info(f"Saved calculation group to {self.history_file}: {group}")
        except Exception as e:
            logger.error(f"Failed to save calculation group to {self.history_file}: {str(e)}")
    
    def get_history(self):
        """Return the list of calculation groups."""
        return self.history
    
    def get_previous_result(self, n):
        """Return the result of the n-th calculation group (n=1 for first calculation)."""
        try:
            if not self.history:
                logger.warn("No previous calculations available")
                raise ValueError("No previous calculations available")
            if n <= 0:
                logger.warn(f"Invalid history index: {n}")
                raise ValueError("History index must be positive")
            if n > len(self.history):
                logger.warn(f"History index {n} out of range; only {len(self.history)} calculations available")
                raise ValueError(f"History index {n} out of range")
            result = self.history[n - 1]['result']  # 1-based indexing
            logger.debug(f"Retrieved previous result (ans({n})): {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to retrieve previous result (ans({n})): {str(e)}")
            raise ValueError(f"Failed to retrieve previous result: {str(e)}")
    
    def save_history_to_file(self):
        """Save the current history to a timestamped backup file."""
        try:
            if not self.history:
                logger.warn("No history to save")
                raise ValueError("No history to save")
            backup_dir = os.path.join(os.path.dirname(self.history_file), 'history_backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                logger.info(f"Created backup directory: {backup_dir}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"history_{timestamp}.json")
            with open(backup_file, 'w') as f:
                json.dump(self.history, f, indent=4)
            logger.info(f"Saved history to {backup_file}")
            return backup_file
        except Exception as e:
            logger.error(f"Failed to save history to backup file: {str(e)}")
            raise ValueError(f"Failed to save history: {str(e)}")
    
    def new_history(self):
        """Clear the current history and start a new one."""
        try:
            self.history = []
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
            logger.info(f"Cleared history and started new history in {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to start new history in {self.history_file}: {str(e)}")
            raise ValueError(f"Failed to start new history: {str(e)}")
    
    def delete_calculation(self, n):
        """Delete the n-th calculation group (n=1 for first calculation)."""
        try:
            if not self.history:
                logger.warn("No history to delete from")
                raise ValueError("No history to delete from")
            if n <= 0:
                logger.warn(f"Invalid history index for deletion: {n}")
                raise ValueError("History index must be positive")
            if n > len(self.history):
                logger.warn(f"History index {n} out of range; only {len(self.history)} calculations available")
                raise ValueError(f"History index {n} out of range")
            deleted_group = self.history.pop(n - 1)  # 1-based indexing
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
            logger.info(f"Deleted calculation {n} from {self.history_file}: {deleted_group}")
        except Exception as e:
            logger.error(f"Failed to delete calculation {n} from {self.history_file}: {str(e)}")
            raise ValueError(f"Failed to delete calculation: {str(e)}")
    
    def load_history_from_file(self, filename):
        """Load history from a specified backup file."""
        try:
            backup_dir = os.path.join(os.path.dirname(self.history_file), 'history_backups')
            backup_file = os.path.join(backup_dir, filename)
            if not os.path.exists(backup_file):
                logger.warn(f"Backup file {backup_file} does not exist")
                raise ValueError(f"Backup file {filename} does not exist")
            with open(backup_file, 'r') as f:
                self.history = json.load(f)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
            logger.info(f"Loaded history from {backup_file} into {self.history_file}: {len(self.history)} entries")
        except Exception as e:
            logger.error(f"Failed to load history from {backup_file}: {str(e)}")
            raise ValueError(f"Failed to load history: {str(e)}")
