# file_analyzer/analyzer/log_analyzer.py
import re
import logging
from analyzer.base import BaseAnalyzer

logger = logging.getLogger(__name__)


class LogFileAnalyzer(BaseAnalyzer):
    def analyze(self):
        try:
            logger.info(f"Analyzing log file: {self.filepath}")
            error_pattern = re.compile(r"^ERROR")
            info_pattern = re.compile(r"^INFO")
            warning_pattern = re.compile(r"^WARNING")
            error_count = 0
            info_count = 0
            line_count = 0
            size_bytes = 0
            warning_count = 0
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line_count += 1
                    size_bytes += len(line.encode("utf-8"))
                    if error_pattern.match(line):
                        error_count += 1
                    elif info_pattern.match(line):
                        info_count += 1
                    elif warning_pattern.match(line):
                        warning_count += 1

                return {
                    "file": self.filepath,
                    "type": "log",
                    "lines": line_count,
                    "error_count": error_count,
                    "info_count": info_count,
                    "warning_count": warning_count,
                    "size_bytes": size_bytes,
                }

        except Exception as e:
            logger.error(f"Erorr Analyzing file {self.filepath}: {e}")
            return {"file": self.filepath, "type": "log", "error": str(e)}
