class OperationError(Exception):
    """Raised for errors during mathematical operations (e.g., invalid operator, mixed precedence)."""
    pass

class CalculatorError(Exception):
    """Raised for errors in input parsing or calculator logic (e.g., invalid format, invalid ans(n))."""
    pass

class HistoryError(Exception):
    """Raised for errors in history management (e.g., invalid index, empty history, file issues)."""
    pass
