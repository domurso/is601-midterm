import pytest
from unittest.mock import patch
from app.memento import CalculationHistory, CalculationMemento
from app.exceptions import HistoryError
from app.config import HISTORY_FILE_PATH, HISTORY_BACKUP_DIR
import pandas as pd
import os

def test_load_history(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    df = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T18:20:58.123456', 
         'steps': '[{"input": "1 + 2", "operation": "+", "a": 1.0, "b": 2.0, "result": 3.0}]'}
    ])
    df.to_csv(history_file, index=False)
    history = CalculationHistory(str(history_file))
    assert len(history.get_history()) == 1
    assert history.get_history().iloc[0]['input'] == '1 + 2'
    assert history.get_history().iloc[0]['result'] == 3.0

def test_load_history_invalid_json(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    df = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T18:20:58.123456', 'steps': 'invalid_json'}
    ])
    df.to_csv(history_file, index=False)
    history = CalculationHistory(str(history_file))
    assert len(history.get_history()) == 1
    assert history.get_history().iloc[0]['steps'] == []

def test_load_history_missing_file(tmp_path):
    history_file = tmp_path / "nonexistent.csv"
    history = CalculationHistory(str(history_file))
    assert history.get_history().empty

def test_load_history_permission_error(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    df = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T18:20:58.123456', 
         'steps': '[{"input": "1 + 2", "operation": "+", "a": 1.0, "b": 2.0, "result": 3.0}]'}
    ])
    df.to_csv(history_file, index=False)
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.side_effect = PermissionError("Permission denied")
        with pytest.raises(HistoryError, match="Failed to load history: Permission denied"):
            CalculationHistory(str(history_file))

def test_load_history_malformed_csv(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    with open(history_file, 'w') as f:
        f.write("input,result,timestamp,steps\n1 + 2,invalid,2025-06-30T18:20:58.123456,[]\n")
    with pytest.raises(HistoryError, match="Failed to load history: Malformed CSV file"):
        CalculationHistory(str(history_file))

def test_save_calculation_group(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    memento = CalculationMemento("1 + 2", "+", 1.0, 2.0, 3.0)
    history.save_calculation_group("1 + 2", 3.0, [memento])
    assert len(history.get_history()) == 1
    assert history.get_history().iloc[0]['input'] == "1 + 2"
    assert history.get_history().iloc[0]['result'] == 3.0
    assert len(history.get_history().iloc[0]['steps']) == 1

def test_save_calculation_group_permission_error(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    memento = CalculationMemento("1 + 2", "+", 1.0, 2.0, 3.0)
    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        mock_to_csv.side_effect = PermissionError("Permission denied")
        with pytest.raises(HistoryError, match="Failed to save calculation group: Permission denied"):
            history.save_calculation_group("1 + 2", 3.0, [memento])

def test_save_history_to_file_permission_error(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    memento = CalculationMemento("1 + 2", "+", 1.0, 2.0, 3.0)
    history.save_calculation_group("1 + 2", 3.0, [memento])
    with patch("os.makedirs") as mock_makedirs:
        mock_makedirs.side_effect = PermissionError("Permission denied")
        with pytest.raises(HistoryError, match="Failed to save history: Permission denied"):
            history.save_history_to_file()

def test_load_history_missing_steps_column(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    df = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T18:20:58.123456'}
    ])
    df.to_csv(history_file, index=False)
    history = CalculationHistory(str(history_file))
    assert len(history.get_history()) == 1
    assert history.get_history().iloc[0]['steps'] == []

def test_get_previous_result_negative_index(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    with pytest.raises(HistoryError, match=r"Invalid history index: 0"):
        history.get_previous_result(0)

def test_get_previous_result_out_of_range(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    memento = CalculationMemento("1 + 2", "+", 1.0, 2.0, 3.0)
    history.save_calculation_group("1 + 2", 3.0, [memento])
    with pytest.raises(HistoryError, match="History index 2 out of range"):
        history.get_previous_result(2)

def test_delete_calculation_empty_history(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    with pytest.raises(HistoryError, match="No history to delete from"):
        history.delete_calculation(1)

def test_delete_calculation_negative_index(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    memento = CalculationMemento("1 + 2", "+", 1.0, 2.0, 3.0)
    history.save_calculation_group("1 + 2", 3.0, [memento])
    with pytest.raises(HistoryError, match=r"Invalid history index: 0"):
        history.delete_calculation(0)

def test_load_history_from_file_malformed_csv(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    backup_file = tmp_path / "history_backups" / "history_20250630_182058.csv"
    os.makedirs(tmp_path / "history_backups")
    with open(backup_file, 'w') as f:
        f.write("input,result,timestamp,steps\n1 + 2,invalid,2025-06-30T18:20:58.123456,[]\n")
    history = CalculationHistory(str(history_file))
    with pytest.raises(HistoryError, match="Failed to load history: Malformed CSV file"):
        history.load_history_from_file("history_20250630_182058.csv")
