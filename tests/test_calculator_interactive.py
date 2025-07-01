import pytest
from unittest.mock import patch, Mock
from app.calculator import calculator
from app.exceptions import CalculatorError, HistoryError
import pandas as pd
import re

def strip_ansi_codes(text):
    ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_regex.sub('', text)

@pytest.fixture
def mock_history():
    mock = Mock()
    mock.get_history.return_value = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
    return mock

def test_calculator_help(mock_history, capteesys):
    with patch("builtins.input", side_effect=["help", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Welcome To Dom Urso's Calculator" in captured
    assert "Supported Operators" in captured

def test_calculator_precedence(mock_history, capteesys):
    with patch("builtins.input", side_effect=["precedence", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Precedence groups define the order of operations" in captured

def test_calculator_history_empty(mock_history, capteesys):
    with patch("builtins.input", side_effect=["history", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "No calculations in history" in captured

def test_calculator_invalid_command(mock_history, capteesys):
    with patch("builtins.input", side_effect=["invalid", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Invalid command: Input must start with a number or ans" in captured

def test_calculator_delete_invalid_index(mock_history, capteesys):
    mock_history.delete_calculation.side_effect = HistoryError("History index 1 out of range")
    with patch("builtins.input", side_effect=["delete 1", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Error: History index 1 out of range" in captured

# def test_calculator_observer_notification(mock_history, capteesys):
#     mock_history.get_history.return_value = pd.DataFrame([
#         {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T22:13:58.123456', 
#          'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
#     ])
#     mock_history.get_previous_result.side_effect = lambda n: 3.0 if n == 1 else HistoryError("Invalid index")
#     with patch("builtins.input", side_effect=["1 + 2", "exit"]):
#         with pytest.raises(SystemExit):
#             calculator(mock_history)
#     captured = strip_ansi_codes(capteesys.readouterr().out)
#     assert "New calculation added: 1 + 2 = 3.0" in captured
#     assert "Step 1: 1 + 2 = 3.0" in captured
#     assert "Result: 3.0" in captured
