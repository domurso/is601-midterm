import os

# Directory for history files relative to project root
HISTORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

# History file name
HISTORY_FILE = 'calculation_history.csv'

# Full path to history file
HISTORY_FILE_PATH = os.path.join(HISTORY_DIR, HISTORY_FILE)

# Backup directory for history files
HISTORY_BACKUP_DIR = os.path.join(HISTORY_DIR, 'history_backups')
