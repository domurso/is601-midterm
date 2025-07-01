import pytest
from unittest.mock import Mock, patch
from app.calculator import calculate_expression
from app.exceptions import CalculatorError, HistoryError, OperationError
from app.config import HISTORY_BACKUP_DIR
import pandas as pd
import os

@pytest.fixture
def mock_history():
    mock = Mock()
    mock.get_history.return_value = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
    return mock

def test_calculate_expression(mock_history):
    mock_history.get_history.return_value = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T22:18:58.123456', 
         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
    ])
    mock_history.get_previous_result.side_effect = lambda n: 3.0 if n == 1 else HistoryError("Invalid index")
    result = calculate_expression("1 + 2", mock_history)
    assert result == 3.0
    mock_history.save_calculation_group.assert_called_once()
    args, _ = mock_history.save_calculation_group.call_args
    assert args[0] == "1 + 2"
    assert args[1] == 3.0
    assert len(args[2]) == 1
    assert args[2][0].get_state()['input'] == "1 + 2"
    assert args[2][0].get_state()['a'] == 1.0
    assert args[2][0].get_state()['b'] == 2.0
    assert args[2][0].get_state()['result'] == 3.0

def test_ans_reference(mock_history):
    mock_history.get_history.return_value = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T22:18:58.123456', 
         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
    ])
    mock_history.get_previous_result.side_effect = lambda n: 3.0 if n == 1 else HistoryError("Invalid index")
    result = calculate_expression("ans(1) * 2", mock_history)
    assert result == 6.0
    mock_history.get_previous_result.assert_called_once_with(1)
    args, _ = mock_history.save_calculation_group.call_args
    assert args[0] == "ans(1) * 2"
    assert args[1] == 6.0
    assert len(args[2]) == 1
    assert args[2][0].get_state()['input'] == "ans(1) (3.0) * 2"
    assert args[2][0].get_state()['a'] == 3.0
    assert args[2][0].get_state()['b'] == 2.0
    assert args[2][0].get_state()['result'] == 6.0

def test_invalid_ans_reference(mock_history):
    mock_history.get_history.return_value = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
    mock_history.get_previous_result.side_effect = HistoryError("No previous calculations available")
    with pytest.raises(HistoryError, match="No previous calculations available"):
        calculate_expression("ans(1) + 2", mock_history)

def test_save_history(mock_history, tmp_path):
    from app.history import save_history
    mock_history.get_history.return_value = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T22:18:58.123456', 
         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
    ])
    backup_file = os.path.join(tmp_path, "history_20250630_221858.csv")
    mock_history.save_history_to_file.return_value = backup_file
    save_history(mock_history)
    mock_history.save_history_to_file.assert_called_once()

def test_load_history_failure(mock_history):
    from app.history import load_history
    mock_history.load_history_from_file.side_effect = HistoryError("Backup file nonexistent.csv does not exist")
    with pytest.raises(HistoryError, match="Backup file nonexistent.csv does not exist"):
        load_history(mock_history, "nonexistent.csv")

# def test_invalid_operator(mock_history):
#     with pytest.raises(ValueError, match="Unsupported calculation"):
#         calculate_expression("1 @ 2", mock_history)

def test_mixed_precedence(mock_history):
    with pytest.raises(OperationError, match="Mixed operator precedence not allowed"):
        calculate_expression("1 + 2 * 3", mock_history)

def test_invalid_format_empty_input(mock_history):
    with pytest.raises(CalculatorError, match="Invalid format"):
        calculate_expression("1 +", mock_history)

def test_invalid_first_token(mock_history):
    with pytest.raises(CalculatorError, match="Invalid command: Input must start with a number or ans"):
        calculate_expression("abc + 2", mock_history)
