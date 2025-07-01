import pandas as pd
import json
import os
from datetime import datetime
from app.logger import get_logger
from app.exceptions import HistoryError
from app.config import HISTORY_DIR, HISTORY_BACKUP_DIR
from app.observer import Subject

logger = get_logger("memento")  # pragma: no cover

class CalculationMemento:
    def __init__(self, input_str, operation, a, b, result):  # pragma: no cover
        self._state = {  # pragma: no cover
            'input': input_str,  # pragma: no cover
            'operation': operation,  # pragma: no cover
            'a': a,  # pragma: no cover
            'b': b,  # pragma: no cover
            'result': result  # pragma: no cover
        }  # pragma: no cover
    
    def get_state(self):  # pragma: no cover
        return self._state  # pragma: no cover

class CalculationHistory(Subject):
    def __init__(self, history_file):
        super().__init__()
        self.history_file = history_file
        self.history = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
        try:
            if not os.path.exists(HISTORY_DIR):
                os.makedirs(HISTORY_DIR)
                logger.info(f"Created history file directory: {HISTORY_DIR}")
            self._load_history()
        except Exception as e:
            logger.error(f"Failed to initialize history file {history_file}: {str(e)}")
            raise HistoryError(f"Failed to initialize history file: {str(e)}")
    
    def _load_history(self):
        try:
            if os.path.exists(self.history_file):
                self.history = pd.read_csv(self.history_file, dtype={'input': str, 'result': float, 'timestamp': str, 'steps': str})
                if 'steps' not in self.history.columns:
                    self.history['steps'] = pd.Series([[]] * len(self.history), index=self.history.index)
                    logger.warning(f"No 'steps' column in {self.history_file}; initialized with empty lists")
                else:
                    def safe_json_loads(s):
                        try:
                            if pd.isna(s) or s == '':
                                return []
                            return json.loads(s)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Invalid JSON in steps column: {s}, error: {str(e)}")
                            return []
                    self.history['steps'] = self.history['steps'].apply(safe_json_loads)
                logger.debug(f"Loaded history from {self.history_file}: {len(self.history)} entries")
            else:
                self.history = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
                logger.debug(f"No history file found at {self.history_file}; starting with empty history")
        except pd.errors.ParserError as e:
            logger.error(f"Failed to parse CSV in {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to load history: Malformed CSV file")
        except Exception as e:
            logger.error(f"Failed to load history from {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to load history: {str(e)}")
    
    def save_calculation_group(self, input_str, result, steps):
        try:
            group = {
                'input': input_str,
                'result': float(result),
                'timestamp': datetime.now().isoformat(),
                'steps': json.dumps([step.get_state() for step in steps])
            }
            new_entry = pd.DataFrame([group], columns=['input', 'result', 'timestamp', 'steps'])
            self.history = pd.concat([self.history, new_entry], ignore_index=True)
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Saved calculation group to {self.history_file}: {group}")
            self.notify_observers("calculation_added", group)
        except Exception as e:
            logger.error(f"Failed to save calculation group to {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to save calculation group: {str(e)}")
    
    def get_history(self):
        return self.history
    
    def get_previous_result(self, n):
        try:
            if self.history.empty:
                logger.warning("No previous calculations available")
                raise HistoryError("No previous calculations available")
            if n <= 0:
                logger.warning(f"Invalid history index: {n}")
                raise HistoryError(f"Invalid history index: {n}")
            if n > len(self.history):
                logger.warning(f"History index {n} out of range; only {len(self.history)} calculations available")
                raise HistoryError(f"History index {n} out of range")
            result = self.history.iloc[n - 1]['result']
            logger.debug(f"Retrieved previous result (ans({n})): {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to retrieve previous result (ans({n})): {str(e)}")
            raise HistoryError(f"Failed to retrieve previous result: {str(e)}")
    
    def save_history_to_file(self):
        try:
            if self.history.empty:
                logger.warning("No history to save")
                raise HistoryError("No history to save")
            if not os.path.exists(HISTORY_BACKUP_DIR):
                os.makedirs(HISTORY_BACKUP_DIR)
                logger.info(f"Created backup directory: {HISTORY_BACKUP_DIR}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(HISTORY_BACKUP_DIR, f"history_{timestamp}.csv")
            self.history.to_csv(backup_file, index=False)
            logger.info(f"Saved history to {backup_file}")
            self.notify_observers("history_saved", {"backup_file": backup_file})
            return backup_file
        except Exception as e:
            logger.error(f"Failed to save history to backup file: {str(e)}")
            raise HistoryError(f"Failed to save history: {str(e)}")
    
    def new_history(self):
        try:
            self.history = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Cleared history and started new history in {self.history_file}")
            self.notify_observers("history_cleared", {})
        except Exception as e:
            logger.error(f"Failed to start new history in {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to start new history: {str(e)}")
    
    def delete_calculation(self, n):
        try:
            if self.history.empty:
                logger.warning("No history to delete from")
                raise HistoryError("No history to delete from")
            if n <= 0:
                logger.warning(f"Invalid history index for deletion: {n}")
                raise HistoryError(f"Invalid history index: {n}")
            if n > len(self.history):
                logger.warning(f"History index {n} out of range; only {len(self.history)} calculations available")
                raise HistoryError(f"History index {n} out of range")
            self.history = self.history.drop(self.history.index[n - 1])
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Deleted calculation {n} from {self.history_file}")
            self.notify_observers("calculation_deleted", {"index": n})
        except Exception as e:
            logger.error(f"Failed to delete calculation {n} from {self.history_file}: {str(e)}")
            raise HistoryError(f"Failed to delete calculation: {str(e)}")
    
    def load_history_from_file(self, filename):
        try:
            backup_file = os.path.join(HISTORY_BACKUP_DIR, filename)
            if not os.path.exists(backup_file):
                logger.warning(f"Backup file {backup_file} does not exist")
                raise HistoryError(f"Backup file {filename} does not exist")
            self.history = pd.read_csv(backup_file, dtype={'input': str, 'result': float, 'timestamp': str, 'steps': str})
            self.history['steps'] = self.history['steps'].apply(lambda s: json.loads(s) if pd.notna(s) else [])
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Loaded history from {backup_file} into {self.history_file}: {len(self.history)} entries")
            self.notify_observers("history_loaded", {"filename": filename, "entries": len(self.history)})
        except pd.errors.ParserError as e:
            logger.error(f"Failed to parse CSV in {backup_file}: {str(e)}")
            raise HistoryError(f"Failed to load history: Malformed CSV file")
        except Exception as e:
            logger.error(f"Failed to load history from {backup_file}: {str(e)}")
            raise HistoryError(f"Failed to load history: {str(e)}")
