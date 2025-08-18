import unittest
import tempfile
import os
from analyzer.text_analyzer import TextFileAnalyzer


class TestTextFileAnalyzer(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".txt", mode="w+", encoding="utf-8"
        )
        self.temp_file.write("Hello world!\nThis is a test.\n")
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_analyze_text_file(self):
        analyzer = TextFileAnalyzer(self.temp_file.name)
        result = analyzer.analyze()

        self.assertEqual(result["type"], "text")
        self.assertEqual(result["lines"], 2)
        self.assertEqual(result["words"], 6)
        self.assertIn("size_bytes", result)

    def test_text_analyzer_empty_file(self):
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".txt", mode="w+", encoding="utf-8"
        ) as temp_file:
            filepath = temp_file.name

        analyzer = TextFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["lines"], 0)
        self.assertEqual(result["words"], 0)
        self.assertEqual(result["size_bytes"], 0)
        self.assertEqual(result["type"], "text")

        os.unlink(filepath)

    def test_text_analyzer_unicode(self):
        content = "🌟✨ Hello, 世界! 🌍\nThis is a line with emojis 😄😃"
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".txt", mode="w+", encoding="utf-8"
        ) as temp_file:
            temp_file.write(content)
            filepath = temp_file.name

        analyzer = TextFileAnalyzer(filepath)
        result = analyzer.analyze()

        self.assertEqual(result["lines"], 2)
        self.assertGreater(result["words"], 0)
        self.assertEqual(result["size_bytes"], len(content.encode("utf-8")))
        self.assertEqual(result["type"], "text")

        os.unlink(filepath)


if __name__ == "__main__":
    unittest.main()
