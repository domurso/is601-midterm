import pandas as pd
import json
import os
from datetime import datetime
from app.logger import get_logger
from app.exceptions import HistoryError

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
    """Caretaker class to manage saving and retrieving calculation groups using pandas."""
    def __init__(self, history_file):
        self.history_file = history_file
        self.history = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
        # Ensure the directory for the history file exists
        history_dir = os.path.dirname(history_file)
        try:
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
                logger.info(f"Created history file directory: {history_dir}")
            self._load_history()
        except Exception as e:
            logger.error(f"Failed to initialize history file {history_file}: {str(e)}")
            raise HistoryError(f"Failed to initialize history file: {str(e)}")
    
    def _load_history(self):
        """Load history from the CSV file."""
        try:
            if os.path.exists(self.history_file):
                self.history = pd.read_csv(self.history_file)
                # Ensure 'steps' column exists
                if 'steps' not in self.history.columns:
                    self.history['steps'] = pd.Series([[]] * len(self.history), index=self.history.index)
                    logger.warn(f"No 'steps' column in {self.history_file}; initialized with empty lists")
                else:
                    # Convert steps from JSON strings to lists of dicts
                    def safe_json_loads(s):
                        try:
                            if pd.isna(s) or s == '':
                                return []
                            return json.loads(s)
                        except json.JSONDecodeError as e:
                            logger.warn(f"Invalid JSON in steps column: {s}, error: {str(e)}")
                            return []
                    self.history['steps'] = self.history['steps'].apply(safe_json_loads)
                logger.debug(f"Loaded history from {self.history_file}: {len(self.history)} entries")
            else:
                self.history = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
                logger.debug(f"No history file found at {self.history_file}; starting with empty history")
        except Exception as e:
            logger.error(f"Failed to load history from {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to load history: {str(e)}")
    
    def save_calculation_group(self, input_str, result, steps):
        """Save a calculation group to the history DataFrame and CSV file."""
        try:
            group = {
                'input': input_str,
                'result': result,
                'timestamp': datetime.now().isoformat(),
                'steps': json.dumps([step.get_state() for step in steps])  # Explicitly serialize to JSON
            }
            # Append to DataFrame
            self.history = pd.concat([self.history, pd.DataFrame([group])], ignore_index=True)
            # Save to CSV
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Saved calculation group to {self.history_file}: {group}")
        except Exception as e:
            logger.error(f"Failed to save calculation group to {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to save calculation group: {str(e)}")
    
    def get_history(self):
        """Return the history DataFrame."""
        return self.history
    
    def get_previous_result(self, n):
        """Return the result of the n-th calculation group (n=1 for first calculation)."""
        try:
            if self.history.empty:
                logger.warn("No previous calculations available")
                raise HistoryError("No previous calculations available")
            if n <= 0:
                logger.warn(f"Invalid history index: {n}")
                raise HistoryError("History index must be positive")
            if n > len(self.history):
                logger.warn(f"History index {n} out of range; only {len(self.history)} calculations available")
                raise HistoryError(f"History index {n} out of range")
            result = self.history.iloc[n - 1]['result']  # 1-based indexing
            logger.debug(f"Retrieved previous result (ans({n})): {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to retrieve previous result (ans({n})): {str(e)}")
            raise HistoryError(f"Failed to retrieve previous result: {str(e)}")
    
    def save_history_to_file(self):
        """Save the current history to a timestamped backup CSV file."""
        try:
            if self.history.empty:
                logger.warn("No history to save")
                raise HistoryError("No history to save")
            backup_dir = os.path.join(os.path.dirname(self.history_file), 'history_backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                logger.info(f"Created backup directory: {backup_dir}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"history_{timestamp}.csv")
            self.history.to_csv(backup_file, index=False)
            logger.info(f"Saved history to {backup_file}")
            return backup_file
        except Exception as e:
            logger.error(f"Failed to save history to backup file: {str(e)}")
            raise HistoryError(f"Failed to save history: {str(e)}")
    
    def new_history(self):
        """Clear the current history and start a new one."""
        try:
            self.history = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Cleared history and started new history in {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to start new history in {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to start new history: {str(e)}")
    
    def delete_calculation(self, n):
        """Delete the n-th calculation group (n=1 for first calculation)."""
        try:
            if self.history.empty:
                logger.warn("No history to delete from")
                raise HistoryError("No history to delete from")
            if n <= 0:
                logger.warn(f"Invalid history index for deletion: {n}")
                raise HistoryError("History index must be positive")
            if n > len(self.history):
                logger.warn(f"History index {n} out of range; only {len(self.history)} calculations available")
                raise HistoryError(f"History index {n} out of range")
            self.history = self.history.drop(self.history.index[n - 1])  # 1-based indexing
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Deleted calculation {n} from {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to delete calculation {n} from {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to delete calculation: {str(e)}")
    
    def load_history_from_file(self, filename):
        """Load history from a specified backup CSV file."""
        try:
            backup_dir = os.path.join(os.path.dirname(self.history_file), 'history_backups')
            backup_file = os.path.join(backup_dir, filename)
            if not os.path.exists(backup_file):
                logger.warn(f"Backup file {backup_file} does not exist")
                raise HistoryError(f"Backup file {filename} does not exist")
            self.history = pd.read_csv(backup_file)
            self.history['steps'] = self.history['steps'].apply(lambda s: json.loads(s) if pd.notna(s) else [])
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Loaded history from {backup_file} into {self.history_file}: {len(self.history)} entries")
        except Exception as e:
            logger.error(f"Failed to load history from {backup_file}: {str(e)}")
            raise HistoryError(f"Failed to load history: {str(e)}")
