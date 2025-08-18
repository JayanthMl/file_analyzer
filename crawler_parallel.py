import os
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from analyzer.text_analyzer import TextFileAnalyzer
from analyzer.log_analyzer import LogFileAnalyzer
from analyzer.json_analyzer import JsonFileAnalyzer
from analyzer.yaml_analyzer import YamlFileAnalyzer
from report.writer import ReportWriter

# Constants
MAX_DIR_WORKERS = 4
MAX_FILE_WORKERS = 4

# Analyzer Map
analyzer_map = {
    ".txt": TextFileAnalyzer,
    ".log": LogFileAnalyzer,
    ".json": JsonFileAnalyzer,
    ".yaml": YamlFileAnalyzer,
    ".yml": YamlFileAnalyzer,
}

# Thread-safe Queue for directories
dir_queue = Queue()

# Function to analyze a single file (unchanged from before)
def analyze_file(file_path, AnalyzerClass):
    try:
        analyzer = AnalyzerClass(file_path)
        result = analyzer.analyze()
        writer = ReportWriter.get_instance()
        writer.add_entry(result)
    except Exception as e:
        ReportWriter.get_instance().add_entry({
            'file': file_path,
            'error': str(e)
        })

# Directory Scanner Worker
def directory_scanner(file_executor, allowed_types):
    while True:
        try:
            current_dir = dir_queue.get(timeout=2)  # timeout to exit if queue is empty
        except:
            break  # Exit if queue is empty and timeout occurs

        try:
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        dir_queue.put(entry.path)
                    elif entry.is_file():
                        ext = os.path.splitext(entry.name)[1].lower()
                        AnalyzerClass = analyzer_map.get(ext)
                        if ext in allowed_types and AnalyzerClass:
                            file_executor.submit(analyze_file, entry.path, AnalyzerClass)
        except Exception as e:
            print(f"Failed to scan directory {current_dir}: {e}")

        dir_queue.task_done()

# Crawl Directory with Parallel Scanning
def crawl_directory_parallel(root_path, allowed_types):
    writer = ReportWriter.get_instance()
    dir_queue.put(root_path)

    with ThreadPoolExecutor(max_workers=MAX_FILE_WORKERS) as file_executor:
        threads = []
        for _ in range(MAX_DIR_WORKERS):
            t = threading.Thread(target=directory_scanner, args=(file_executor, allowed_types))
            t.start()
            threads.append(t)

        # Wait until all directories have been processed
        dir_queue.join()

        # Ensure all directory scanner threads exit
        for t in threads:
            t.join()

        # Wait for all file analysis tasks to finish
        file_executor.shutdown(wait=True)
