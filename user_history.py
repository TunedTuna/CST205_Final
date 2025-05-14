import json
import os
from datetime import datetime

history_file = os.path.join(os.path.dirname(__file__), 'user_history.json')

def log_user_action(username, action, filename=None):
    history = {}
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            history = json.load(file)
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
    }
    if filename:
        entry["filename"] = filename

    history.setdefault(username, []).append(entry)

    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)
