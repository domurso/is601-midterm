import pytest
from unittest.mock import patch
from app.memento import CalculationHistory, CalculationMemento
from app.exceptions import HistoryError
import pandas as pd

def test_load_history(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    # Create a sample CSV
    df = pd.DataFrame([
        {'input': '1 + 2', 'result': 3.0, 'timestamp': '2025-06-30T17:30:56.123456', 
         'steps': '[{"input": "1 + 2", "operation": "+", "a": 1.0, "b": 2.0, "result": 3.0}]'}
    ])
    df.to_csv(history_file, index=False)

    history = CalculationHistory(str(history_file))
    assert len(history.get_history()) == 1
    assert history.get_history().iloc[0]['result'] == 3.0

def test_load_history_missing_file(tmp_path):
    history_file = tmp_path / "nonexistent.csv"
    history = CalculationHistory(str(history_file))
    assert history.get_history().empty

def test_save_calculation_group(tmp_path):
    history_file = tmp_path / "calculation_history.csv"
    history = CalculationHistory(str(history_file))
    memento = CalculationMemento("1 + 2", "+", 1.0, 2.0, 3.0)
    history.save_calculation_group("1 + 2", 3.0, [memento])
    assert len(history.get_history()) == 1
    assert history.get_history().iloc[0]['input'] == "1 + 2"
