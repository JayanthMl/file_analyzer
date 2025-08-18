# file_analyzer/analyzer/base.py

from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def analyze(self):
        pass
