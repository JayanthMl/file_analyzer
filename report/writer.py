# file_analyzer/report/writer.py

import json
import threading


class ReportWriter:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.entries = []

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = ReportWriter()
            return cls._instance

    def init_output(self):
        self.entries = []

    def add_entry(self, data):
        self.entries.append(data)

    def save_output(self, filename="analysis_report.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2)
        print(f"Saved report to {filename}")
