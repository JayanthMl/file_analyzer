# tests/test_log_analyzer.py

import unittest
import tempfile
import os
from analyzer.log_analyzer import LogFileAnalyzer


class TestLogFileAnalyzer(unittest.TestCase):
    def create_temp_log(self, content):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".log", mode="w+", encoding="utf-8"
        )
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_log_file_with_errors_and_warnings(self):
        content = "INFO: System started\nWARNING: Low memory\nERROR: Disk failure"
        filepath = self.create_temp_log(content)

        analyzer = LogFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "log")
        self.assertEqual(result["lines"], 3)
        self.assertEqual(result["error_count"], 1)
        self.assertEqual(result["warning_count"], 1)
        self.assertIn("size_bytes", result)

        os.unlink(filepath)

    def test_log_file_empty(self):
        filepath = self.create_temp_log("")

        analyzer = LogFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["lines"], 0)
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["warning_count"], 0)
        self.assertEqual(result["type"], "log")

        os.unlink(filepath)

    def test_log_file_only_info(self):
        content = "INFO: Started\nINFO: Running\nINFO: Done"
        filepath = self.create_temp_log(content)

        analyzer = LogFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["lines"], 3)
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["warning_count"], 0)
        self.assertEqual(result["type"], "log")

        os.unlink(filepath)


if __name__ == "__main__":
    unittest.main()
