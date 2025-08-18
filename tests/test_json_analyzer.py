import unittest
import tempfile
import os
import json
from analyzer.json_analyzer import JsonFileAnalyzer


class TestJsonFileAnalyzer(unittest.TestCase):
    def create_temp_json(self, data):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".json", mode="w+", encoding="utf-8"
        )
        json.dump(data, temp_file)
        temp_file.close()
        return temp_file.name

    def test_flat_json_object(self):
        data = {"a": 1, "b": 2}
        filepath = self.create_temp_json(data)

        analyzer = JsonFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "json")
        self.assertEqual(result["top_level_keys"], ["a", "b"])
        self.assertEqual(result["total_elements"], 2)
        self.assertEqual(result["total_keys"], 2)

        os.unlink(filepath)

    def test_nested_json_object(self):
        data = {"a": {"b": 1, "c": {"d": 2}}, "e": 3}
        filepath = self.create_temp_json(data)

        analyzer = JsonFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "json")
        self.assertEqual(result["top_level_keys"], ["a", "e"])
        self.assertEqual(result["total_elements"], 2)
        self.assertEqual(result["total_keys"], 5)  # a, b, c, d, e

        os.unlink(filepath)

    def test_json_array(self):
        data = [{"a": 1}, {"b": 2, "c": {"d": 3}}]
        filepath = self.create_temp_json(data)

        analyzer = JsonFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "json")
        self.assertEqual(result["top_level_keys"], [])
        self.assertEqual(result["total_elements"], 2)
        self.assertEqual(result["total_keys"], 4)

        os.unlink(filepath)

    def test_invalid_json(self):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".json", mode="w+", encoding="utf-8"
        )
        temp_file.write("{invalid_json: true")  # invalid JSON
        temp_file.close()

        analyzer = JsonFileAnalyzer(temp_file.name)
        result = analyzer.analyze()

        self.assertIn("error", result)
        self.assertEqual(result["type"], "json")

        os.unlink(temp_file.name)


if __name__ == "__main__":
    unittest.main()
