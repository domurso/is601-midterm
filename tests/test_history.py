import pytest
from unittest.mock import Mock
from app.history import display_history, save_history, new_history, delete_calculation, load_history, HistoryDisplayObserver
from app.exceptions import HistoryError
import pandas as pd
import os
from colorama import Fore, Style
import re

def strip_ansi_codes(text):
    ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_regex.sub('', text)

@pytest.fixture
def mock_history():
    mock = Mock()
    mock.get_history.return_value = pd.DataFrame(columns=['input', 'result', 'timestamp', 'steps'])
    return mock

def test_display_history_empty(mock_history, capteesys):
    display_history(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "No calculations in history" in captured

def test_display_history_with_data(mock_history, capteesys):
    mock_history.get_history.return_value = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T22:18:58.123456', 
         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]}
    ])
    display_history(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Calculation History:" in captured
    assert "1 + 2 = 3.0" in captured
    assert "Step 1: 1 + 2 = 3.0" in captured

def test_display_history_error(mock_history, capteesys):
    mock_history.get_history.side_effect = Exception("Test error")
    with pytest.raises(HistoryError, match="Failed to display history: Test error"):
        display_history(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Failed to display history: Test error" in captured

def test_save_history(mock_history, capteesys):
    mock_history.save_history_to_file.return_value = "logs/history_backups/history_20250630_221858.csv"
    save_history(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "History saved to" in captured

def test_save_history_error(mock_history, capteesys):
    mock_history.save_history_to_file.side_effect = HistoryError("Failed to save history: No history to save")
    with pytest.raises(HistoryError, match="Failed to save history: No history to save"):
        save_history(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Failed to save history: No history to save" in captured

def test_new_history(mock_history, capteesys):
    new_history(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Started new history" in captured

def test_new_history_error(mock_history, capteesys):
    mock_history.new_history.side_effect = HistoryError("Failed to start new history: Permission denied")
    with pytest.raises(HistoryError, match="Failed to start new history: Permission denied"):
        new_history(mock_history)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Failed to start new history: Permission denied" in captured

def test_delete_calculation(mock_history, capteesys):
    delete_calculation(mock_history, 1)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Deleted calculation 1" in captured

def test_delete_calculation_error(mock_history, capteesys):
    mock_history.delete_calculation.side_effect = HistoryError("History index 1 out of range")
    with pytest.raises(HistoryError, match="History index 1 out of range"):
        delete_calculation(mock_history, 1)
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Failed to delete calculation 1: History index 1 out of range" in captured

def test_load_history(mock_history, capteesys):
    load_history(mock_history, "history_20250630_221858.csv")
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Loaded history from" in captured

def test_load_history_error(mock_history, capteesys):
    mock_history.load_history_from_file.side_effect = HistoryError("Backup file nonexistent.csv does not exist")
    with pytest.raises(HistoryError, match="Backup file nonexistent.csv does not exist"):
        load_history(mock_history, "nonexistent.csv")
    captured = strip_ansi_codes(capteesys.readouterr().out)
    assert "Failed to load history from nonexistent.csv: Backup file nonexistent.csv does not exist" in captured

# def test_history_display_observer_calculation_added(mock_history, capteesys):
#     observer = HistoryDisplayObserver()
#     mock_history.register_observer(observer)
#     mock_history.notify_observers("calculation_added", {
#         'input': '1 + 2',
#         'result': 3.0,
#         'timestamp': '2025-06-30T22:18:58.123456',
#         'steps': [{'input': '1 + 2', 'operation': '+', 'a': 1.0, 'b': 2.0, 'result': 3.0}]
#     })
#     captured = strip_ansi_codes(capteesys.readouterr().out)
#     assert "New calculation added: 1 + 2 = 3.0" in captured
#     assert "Step 1: 1 + 2 = 3.0" in captured

# def test_history_display_observer_history_saved(mock_history, capteesys):
#     observer = HistoryDisplayObserver()
#     mock_history.register_observer(observer)
#     mock_history.notify_observers("history_saved", {"backup_file": "logs/history_backups/history_20250630_221858.csv"})
#     captured = strip_ansi_codes(capteesys.readouterr().out)
#     assert "History saved to logs/history_backups/history_20250630_221858.csv" in captured

# def test_history_display_observer_history_cleared(mock_history, capteesys):
#     observer = HistoryDisplayObserver()
#     mock_history.register_observer(observer)
#     mock_history.notify_observers("history_cleared", {})
#     captured = strip_ansi_codes(capteesys.readouterr().out)
#     assert "Started new history" in captured

# def test_history_display_observer_calculation_deleted(mock_history, capteesys):
#     observer = HistoryDisplayObserver()
#     mock_history.register_observer(observer)
#     mock_history.notify_observers("calculation_deleted", {"index": 1})
#     captured = strip_ansi_codes(capteesys.readouterr().out)
#     assert "Deleted calculation 1" in captured

# def test_history_display_observer_history_loaded(mock_history, capteesys):
#     observer = HistoryDisplayObserver()
#     mock_history.register_observer(observer)
#     mock_history.notify_observers("history_loaded", {"filename": "history_20250630_221858.csv", "entries": 1})
#     captured = strip_ansi_codes(capteesys.readouterr().out)
#     assert "Loaded history from history_20250630_221858.csv" in captured
