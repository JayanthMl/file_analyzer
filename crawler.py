# file_analyzer/crawler.py

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from analyzer.text_analyzer import TextFileAnalyzer
from analyzer.log_analyzer import LogFileAnalyzer
from analyzer.json_analyzer import JsonFileAnalyzer
from analyzer.yaml_analyzer import YamlFileAnalyzer
from report.writer import ReportWriter

MAX_WORKERS = 4


def analyze_file(file_path, AnalyzerClass):
    try:
        analyzer = AnalyzerClass(file_path)
        result = analyzer.analyze()
        writer = ReportWriter.get_instance()
        writer.add_entry(result)
    except Exception as e:
        ReportWriter.get_instance().add_entry({"file": file_path, "error": str(e)})


def crawl_directory(path, allowed_types=None):
    if allowed_types is None:
        allowed_types = [".txt", ".log", ".json", "yaml"]
    analyzer_map = {
        ".txt": TextFileAnalyzer,
        ".text": TextFileAnalyzer,
        ".log": LogFileAnalyzer,
        ".logs": LogFileAnalyzer,
        ".json": JsonFileAnalyzer,
        ".yaml": YamlFileAnalyzer,
        ".yml": YamlFileAnalyzer,
    }
    futures = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for root, dirs, files in os.walk(path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                AnalyzerClass = analyzer_map.get(ext)
                if ext in [e.lower() for e in allowed_types] and AnalyzerClass:
                    full_path = os.path.join(root, file)
                    futures.append(
                        executor.submit(analyze_file, full_path, AnalyzerClass)
                    )

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                ReportWriter.get_instance().add_entry(f"Error: {e}")
