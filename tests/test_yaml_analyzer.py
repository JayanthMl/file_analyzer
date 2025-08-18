import unittest
import tempfile
import os
import yaml
from analyzer.yaml_analyzer import YamlFileAnalyzer


class TestYamlFileAnalyzer(unittest.TestCase):
    def create_temp_yaml(self, data):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".yaml", mode="w+", encoding="utf-8"
        )
        yaml.dump(data, temp_file)
        temp_file.close()
        return temp_file.name

    def test_flat_yaml(self):
        data = {"a": 1, "b": 2}
        filepath = self.create_temp_yaml(data)

        analyzer = YamlFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "yaml")
        self.assertEqual(result["top_level_keys"], ["a", "b"])
        self.assertEqual(result["total_elements"], 2)
        self.assertEqual(result["total_keys"], 2)

        os.unlink(filepath)

    def test_nested_yaml(self):
        data = {"a": {"b": {"c": 1}}, "d": 2}
        filepath = self.create_temp_yaml(data)

        analyzer = YamlFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "yaml")
        self.assertEqual(result["top_level_keys"], ["a", "d"])
        self.assertEqual(result["total_elements"], 2)
        self.assertEqual(result["total_keys"], 4)

        os.unlink(filepath)

    def test_yaml_list(self):
        data = [{"a": 1}, {"b": {"c": 2}}]
        filepath = self.create_temp_yaml(data)

        analyzer = YamlFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "yaml")
        self.assertEqual(result["top_level_keys"], [])
        self.assertEqual(result["total_elements"], 2)
        self.assertEqual(result["total_keys"], 3)

        os.unlink(filepath)

    def test_invalid_yaml(self):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".yaml", mode="w+", encoding="utf-8"
        )
        temp_file.write("key: [unclosed list")
        temp_file.close()

        analyzer = YamlFileAnalyzer(temp_file.name)
        result = analyzer.analyze()

        self.assertIn("error", result)
        self.assertEqual(result["type"], "yaml")

        os.unlink(temp_file.name)


if __name__ == "__main__":
    unittest.main()
