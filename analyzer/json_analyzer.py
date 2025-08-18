# file_analyer/analyzer/json_analyzer
import logging
import json
from analyzer.base import BaseAnalyzer

logger = logging.getLogger(__name__)


class JsonFileAnalyzer(BaseAnalyzer):
    def analyze(self):
        try:
            logger.info(f"Analyzing json file: {self.filepath}")
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()
                data = json.loads(content)
                if isinstance(data, dict):
                    top_level_keys = list(data.keys())
                    total_elements = len(data)
                else:
                    top_level_keys = []
                    total_elements = len(data)

                def count_keys(obj):
                    if isinstance(obj, dict):
                        return len(obj) + sum(count_keys(v) for v in obj.values())
                    elif isinstance(obj, list):
                        return sum(count_keys(item) for item in obj)
                    else:
                        return 0

                return {
                    "file": self.filepath,
                    "type": "json",
                    "lines": len(lines),
                    "size_bytes": sum(len(line.encode("utf-8")) for line in lines),
                    "top_level_keys": top_level_keys,
                    "total_elements": total_elements,
                    "total_keys": count_keys(data),
                }
        except Exception as e:
            logger.error(f"Erorr Analyzing file {self.filepath}: {e}")
            return {"file": self.filepath, "type": "json", "error": str(e)}
