import pytest
from unittest.mock import patch, Mock
from app.calculator import calculator
from app.exceptions import CalculatorError, HistoryError
import pandas as pd

@pytest.fixture
def mock_history():
    mock = Mock()
    mock.get_history.return_value = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
    return mock

def test_calculator_help(mock_history, capsys):
    with patch("builtins.input", side_effect=["help", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = capsys.readouterr()
    assert "Welcome To Dom Urso's Calculator" in captured.out
    assert "Supported Operators" in captured.out

def test_calculator_precedence(mock_history, capsys):
    with patch("builtins.input", side_effect=["precedence", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = capsys.readouterr()
    assert "Precedence groups define the order of operations" in captured.out

def test_calculator_history_empty(mock_history, capsys):
    with patch("builtins.input", side_effect=["history", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = capsys.readouterr()
    assert "No calculations in history." in captured.out

def test_calculator_invalid_command(mock_history, capsys):
    with patch("builtins.input", side_effect=["invalid", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = capsys.readouterr()
    assert "Invalid command: Input must start with a number or ans" in captured.out

def test_calculator_delete_invalid_index(mock_history, capsys):
    mock_history.delete_calculation.side_effect = HistoryError("History index 1 out of range")
    with patch("builtins.input", side_effect=["delete 1", "exit"]):
        with pytest.raises(SystemExit):
            calculator(mock_history)
    captured = capsys.readouterr()
    assert "Error: History index 1 out of range" in captured.out
