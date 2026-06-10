"""History persistence manager for snake length leaderboard records."""

import json
import os
import time
from decorators import history_pipeline

class GameHistoryManager:
    """Manage history logging and persistent leaderboard records."""
    def __init__(self, filename="snake_history.json"):
        self.filename = filename

    def load_history(self):
        """Load the persisted leaderboard history from a JSON file."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    @history_pipeline
    def save_record(self, name, score):
        """Save a leaderboard record and sort the table by descending score."""
        history = self.load_history()
        history.append({
            "name": name,
            "score": score,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })


        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=4)
        except IOError as e:
            print(f"[IO EXCEPTION] Failed flushing database pipeline: {e}")
