import pytest
from unittest.mock import Mock, patch
from app.calculator import calculate_expression, history
from app.exceptions import CalculatorError, HistoryError
import pandas as pd

# Mock CalculationHistory to avoid real file I/O
@pytest.fixture
def mock_history():
    with patch("app.calculator.CalculationHistory") as MockHistory:
        # Create a mock instance
        mock_instance = MockHistory.return_value
        # Initialize an empty DataFrame for history
        mock_instance.get_history.return_value = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
        yield mock_instance

def test_calculate_expression(mock_history):
    # Configure mock to simulate saving a calculation
    mock_history.get_history.return_value = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T17:30:56.123456', 
         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
    ])
    mock_history.get_previous_result.side_effect = lambda n: 3.0 if n == 1 else HistoryError("Invalid index")

    # Test a simple calculation
    result = calculate_expression("1 + 2")
    assert result == 3.0
    mock_history.save_calculation_group.assert_called_once()
    # Check the arguments passed to save_calculation_group
    args, _ = mock_history.save_calculation_group.call_args
    assert args[0] == "1 + 2"
    assert args[1] == 3.0
    assert len(args[2]) == 1  # One step
    assert args[2][0].get_state()['input'] == "1 + 2"

def test_ans_reference(mock_history):
    # Simulate a previous result
    mock_history.get_history.return_value = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T17:30:56.123456', 
         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
    ])
    mock_history.get_previous_result.side_effect = lambda n: 3.0 if n == 1 else HistoryError("Invalid index")

    # Test using ans(1)
    result = calculate_expression("ans(1) * 2")
    assert result == 6.0
    mock_history.get_previous_result.assert_called_once_with(1)
    mock_history.save_calculation_group.assert_called_once()
    args, _ = mock_history.save_calculation_group.call_args
    assert args[0] == "ans(1) * 2"
    assert args[1] == 6.0
    assert args[2][0].get_state()['input'] == "ans(1) (3.0) * 2"

def test_invalid_ans_reference(mock_history):
    mock_history.get_history.return_value = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
    mock_history.get_previous_result.side_effect = HistoryError("No previous calculations available")

    with pytest.raises(HistoryError, match="No previous calculations available"):
        calculate_expression("ans(1) + 2")

def test_save_history(mock_history, tmp_path):
    from app.history import save_history
    # Simulate a non-empty history
    mock_history.get_history.return_value = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T17:30:56.123456', 
         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
    ])
    mock_history.save_history_to_file.return_value = str(tmp_path / "history_20250630_173056.csv")

    save_history(mock_history)
    mock_history.save_history_to_file.assert_called_once()

def test_load_history_failure(mock_history):
    from app.history import load_history
    mock_history.load_history_from_file.side_effect = HistoryError("Backup file nonexistent.csv does not exist")

    with pytest.raises(HistoryError, match="Backup file nonexistent.csv does not exist"):
        load_history(mock_history, "nonexistent.csv")
