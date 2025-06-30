Dom Urso's Midterm Calculator
A command-line calculator built in Python, featuring multi-step arithmetic operations, history tracking, and a colorful user interface. The calculator supports operations like addition, subtraction, multiplication, division, modulo, percentage, integer division, power, root, and absolute difference, with a history system to store and recall calculations using ans(n) notation.
Table of Contents


Arithmetic Operations:
Supports + (addition), - (subtraction), -- (absolute difference), * (multiplication), / (division), % (modulo), /% (percentage), // (integer division), ^ (power), ? (root).
Enforces operator precedence in three groups: (+, -, --), (*, /, %, /%, //), (^, ?).


History Management:
Stores calculations in logs/calculation_history.csv using pandas.
Supports ans(n) (1-based indexing) to recall the n-th result and ans for the latest result.
Commands: history (view history), save (save to backup), new (clear history), delete <index> (remove calculation), load <filename> (load backup).


Colored Output:
Blue prompt and welcome message.
Green results and success messages.
Red error messages.
Yellow headers and timestamps, cyan indices in history output.


Error Handling:
Custom exceptions: OperationError, CalculatorError, HistoryError.


Testing:
Comprehensive test suite with pytest and pytest-cov.
Coverage: ~93% for memento.py, ~84% for operations.py, ~79% overall.



Requirements

Python: 3.13.3
Dependencies:
pandas>=2.2.3
python-dotenv>=1.0.1
colorama>=0.4.6
pytest>=8.4.1
pytest-cov>=6.2.1



Install dependencies:
pip install pandas python-dotenv colorama pytest pytest-cov

Setup

Clone the Repository:
git clone <repository-url>
cd project_root


Create a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install pandas python-dotenv colorama pytest pytest-cov


Set Up the .env File:Create project_root/.env with the following content:
LOG_LEVEL=DEBUG
LOG_FILE_PREFIX=app

This configures logging to logs/app-<date>.log with DEBUG level.

Ensure Write Permissions:
chmod -R u+w logs



Operating the Calculator
Run the calculator:
cd project_root
python main.py

Example Interaction (colors indicated in parentheses):
Welcome to Dom Urso's Calculator! (blue)
Enter calculations like '1 + 2 + 3' or 'ans(1) + 2', 'history' to view past calculations, or 'exit' to quit.
>> 1 + 2 (blue)
Result: 3 (green)
>> ans(1) * 2 (blue)
Result: 6 (green)
>> history (blue)
Calculation History: (yellow)
1. (cyan) 2025-06-30T18:55:58.123456 (yellow): 1 + 2 = 3.0
   Step 1 (cyan): 1 + 2 = 3.0
2. (cyan) 2025-06-30T18:55:59.123456 (yellow): ans(1) * 2 = 6.0
   Step 1 (cyan): ans(1) (3.0) * 2 = 6.0
>> save (blue)
History saved to logs/history_backups/history_20250630_185958.csv (green, filename in cyan)
>> delete 1 (blue)
Deleted calculation 1 (green, index in cyan)
>> new (blue)
Started new history (green)
>> load history_20250630_185958.csv (blue)
Loaded history from history_20250630_185958.csv (green, filename in cyan)
>> invalid + 2 (blue)
Error: Invalid command: Input must start with a number or ans(n) (red)
Please try again or type 'help' for assistance (red)
>> help (blue)
Welcome To Dom Urso's Calculator (yellow)
... (help text with green examples and commands)

Commands:

help: Display help with supported operators and commands.
precedence: Show operator precedence groups.
history: View calculation history with steps.
save: Save history to a timestamped CSV in logs/history_backups/.
new: Clear current history.
delete <index>: Remove the calculation at <index> (1-based).
load <filename>: Load history from a backup CSV.
exit: Quit the calculator.

Calculation Format:

Enter expressions like number operator number [operator number]... (e.g., 1 + 2 + 3, ans(1) * 2).
Use ans(n) for the n-th result or ans for the latest.

Running Tests
The project includes a test suite in tests/ to verify functionality using pytest and pytest-cov.

Run Tests:
cd project_root
python -m pytest tests/ --cov=app --cov-report=term --cov-report=html


View Coverage:

Terminal report shows coverage per module (e.g., memento.py: ~93%, operations.py: ~84%, overall: ~79%).
HTML report is generated in htmlcov/. Open it:firefox htmlcov/index.html  # On Windows: start htmlcov\index.html




Test Files:

test_calculator_with_mock.py: Tests calculator.py with mocked history.
test_memento.py: Tests memento.py for history loading/saving.
test_operations.py: Tests operations.py for arithmetic operations.
test_calculator_interactive.py: Tests interactive commands in calculator.py.
test_logger.py: Tests logging configuration.



Example Output:
----------- coverage: platform linux, python 3.13.3-final-0 -----------
Name                 Stmts   Miss  Cover
----------------------------------------
app/__init__.py          0      0   100%
app/calculation.py      14      0   100%
app/calculator.py      180     50    72%
app/config.py            4      0   100%
app/exceptions.py        6      0   100%
app/history.py          53     20    62%
app/logger.py           58     18    69%
app/memento.py         135     10    93%
app/operations.py       62     10    84%
----------------------------------------
TOTAL                  512    108    79%

Troubleshooting:

Tests Fail: Run with verbose output:python -m pytest tests/ -v


History Pollution: Reset logs/calculation_history.csv:echo "input,result,timestamp,steps" > logs/calculation_history.csv


Permissions: Ensure write access to logs/:chmod -R u+w logs



Environment Configuration
Create a .env file in the project root (project_root/.env):
LOG_LEVEL=DEBUG
LOG_FILE_PREFIX=app


LOG_LEVEL: Sets logging level (DEBUG, INFO, etc.). Use DEBUG for detailed logs.
LOG_FILE_PREFIX: Prefix for log files (e.g., app-2025-06-30.log in logs/).

Logs are saved to logs/app-<date>.log for debugging.
Project Structure
project_root/
├── .env
├── logs/
│   ├── app-<date>.log
│   ├── calculation_history.csv
│   ├── history_backups/
│   │   ├── history_<timestamp>.csv
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── config.py
│   ├── exceptions.py
│   ├── history.py
│   ├── logger.py
│   ├── memento.py
│   ├── operations.py
├── tests/
│   ├── test_calculator_with_mock.py
│   ├── test_memento.py
│   ├── test_operations.py
│   ├── test_calculator_interactive.py
│   ├── test_logger.py
├── main.py


app/: Core application modules.
calculator.py: Main calculator logic and CLI interface with colored output.
calculation.py: Factory for creating operation instances.
config.py: Configuration for history file paths.
exceptions.py: Custom exceptions (OperationError, CalculatorError, HistoryError).
history.py: History management functions with colored output.
logger.py: Logging configuration.
memento.py: History storage using pandas.
operations.py: Arithmetic operations with overflow checks excluded from coverage.


logs/: Stores logs and history files.
tests/: Test suite for all modules.
main.py: Entry point to run the calculator.
