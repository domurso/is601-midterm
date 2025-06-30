from app.calculator import calculator
from app.memento import CalculationHistory
from app.config import HISTORY_FILE_PATH

if __name__ == "__main__":
    history = CalculationHistory(HISTORY_FILE_PATH)
    calculator(history)
