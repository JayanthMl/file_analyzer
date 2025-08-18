# file_analyzer/analyzer/text_analyzer.py
import logging
from analyzer.base import BaseAnalyzer

logger = logging.getLogger(__name__)


class TextFileAnalyzer(BaseAnalyzer):
    def analyze(self):
        try:
            logger.info(f"Analyzing text file: {self.filepath}")
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            return {
                "file": self.filepath,
                "type": "text",
                "lines": len(lines),
                "words": sum(len(line.split()) for line in lines),
                "size_bytes": sum(len(line.encode("utf-8")) for line in lines),
            }
        except Exception as e:
            logger.error(f"Erorr Analyzing file {self.filepath}: {e}")
            return {"file": self.filepath, "type": "text", "error": str(e)}
