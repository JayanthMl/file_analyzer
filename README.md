# File Analyzer

## Project Overview
A command-line tool to analyze various file types (`.txt`, `.log`, `.json`, `.yaml`) across directories.  
It recursively scans directories using concurrent threads, analyzes files with type-specific logic, and generates structured reports with performance profiling and error handling.

## Motivation
Many systems generate diverse files needing analysis for monitoring, auditing, or data extraction.  
This tool addresses the need for a fast, extensible, and robust file analyzer to handle multiple formats efficiently, especially in environments with large and deeply nested directory trees.

## Features
- Supports `.txt`, `.log`, `.json`, and `.yaml` file formats with format-specific analyzers.  
- Recursively scans directories with thread pools for concurrency and performance.  
- Generates JSON reports summarizing file statistics and content insights.  
- Handles errors gracefully, logging parsing failures without crashing.  
- Performance profiling identifies and addresses bottlenecks (e.g., YAML parsing, log scanning).  
- Packaged with modern Python tools for easy installation and CLI usage.  
- Comprehensive test suite covering normal and edge cases for reliability.

## Architecture
- **Modular analyzers** inherit from a `BaseAnalyzer` abstract class, facilitating easy extension to new file types.  
- **Crawler** walks directories concurrently, delegating file analysis to worker threads.  
- **ReportWriter** singleton aggregates and outputs analysis results in JSON format.  
- **Concurrency model** uses Python's `ThreadPoolExecutor` for IO-bound parallelism.  
- Profiling tools (`cProfile`) integrated to identify performance hotspots, leading to iterative optimizations.

*Diagram (optional):*  
```

\[Directory Scanner] --> \[Worker Thread Pool] --> \[Analyzers] --> \[Report Aggregator]

````

## Installation & Usage
```bash
# Install package from source wheel
pip install dist/file_analyzer-0.1.0-py3-none-any.whl

# Run CLI tool
file-analyzer --path /path/to/directory --types .txt .log .json .yaml

# Run tests
python -m unittest discover tests
````

## Performance & Profiling

* Initial bottlenecks found in YAML parsing and log file scanning.
* Applied `CSafeLoader` for YAML parsing and compiled regex for logs, resulting in 5x faster YAML and significantly faster log processing.
* File scanning remains the main runtime cost; future plans include parallelizing directory traversal.

## Limitations & Future Work

* Uses Python threading with GIL, limiting CPU-bound scalability.
* No distributed or multi-machine support yet—horizontal scaling is a future goal.
* Basic CLI interface; adding a web API or dashboard could enhance usability.
* Advanced monitoring (logging, metrics) and CI/CD integration not yet implemented.
* Larger datasets and real-time streaming file analysis remain to be explored.

## Learning Outcomes

* Designed and implemented a modular, extensible file analysis system.
* Gained practical experience with Python concurrency, profiling, and optimization.
* Learned packaging and testing best practices for Python CLI tools.
* Developed skills to identify, profile, and resolve performance bottlenecks.
* Improved understanding of multi-format file parsing and error resilience.

## Contact & Feedback

Feel free to reach out for questions or feedback!
\[https://github.com/JayanthMl]



