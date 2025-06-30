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
