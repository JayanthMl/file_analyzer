# file_analyzer/main.py

from crawler import crawl_directory
from report.writer import ReportWriter
from logging_config import setup_logger
import threading
import argparse
from crawler_parallel import crawl_directory_parallel

def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze text and log files in a directory"
    )
    parser.add_argument(
        "--path", type=str, required=True, help="Path to the directory to analyze"
    )
    parser.add_argument(
        "--types",
        nargs="*",
        default=[".txt"],
        help="File extensions to include (default: .txt)",
    )
    return parser.parse_args()


def main():
    # path = input("Enter directory to analyze: ").strip()
    args = parse_args()
    writer = ReportWriter.get_instance()
    writer.init_output()

    # Start crawling in a separate thread for demo
    thread = threading.Thread(target=crawl_directory_parallel, args=(args.path, args.types))
    thread.start()
    thread.join()

    writer.save_output()


if __name__ == "__main__":
    setup_logger()
    main()
