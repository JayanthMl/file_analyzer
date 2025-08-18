import os
import random
import json
import yaml
from pathlib import Path

BASE_DIR = Path("test_data")

TEXT_SNIPPETS = [
    "This is a sample line.",
    "Another line follows here.",
    "Text files are often simple.",
    "Python is great for scripting.",
    "End of sample block."
]

LOG_SNIPPETS = [
    "INFO: System boot complete",
    "WARNING: Disk space low",
    "ERROR: Unable to access database",
    "INFO: User logged in",
    "ERROR: Timeout occurred"
]

YAML_SNIPPETS = [
    {"key": "value"},
    {"service": {"name": "auth", "port": 8080}},
    {"database": {"host": "localhost", "port": 5432}},
    {"logging": {"level": "info", "output": "stdout"}},
    {"features": {"enable_cache": True, "max_items": 100}}
]

JSON_SNIPPETS = [
    {"a": 1, "b": 2},
    {"user": {"id": 1, "name": "Alice"}},
    [{"item": i} for i in range(5)],
    {"metrics": {"cpu": 0.9, "memory": 0.7}},
    {"events": ["start", "stop", "restart"]}
]

def create_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_text_files(dir_path, count=50):
    for i in range(count):
        lines = random.choices(TEXT_SNIPPETS, k=random.randint(10, 100))
        create_file(dir_path / f"file_{i}.txt", "\n".join(lines))

def generate_log_files(dir_path, count=30):
    for i in range(count):
        lines = random.choices(LOG_SNIPPETS, k=random.randint(10, 100))
        create_file(dir_path / f"log_{i}.log", "\n".join(lines))

def generate_yaml_files(dir_path, count=100):
    for i in range(count):
        snippet = random.choice(YAML_SNIPPETS)
        create_file(dir_path / f"config_{i}.yaml", yaml.dump(snippet))

def generate_json_files(dir_path, count=30):
    for i in range(count):
        snippet = random.choice(JSON_SNIPPETS)
        create_file(dir_path / f"data_{i}.json", json.dumps(snippet))

def setup_structure():
    (BASE_DIR / "small_texts").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "logs").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "config" / "environments" / "dev").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "config" / "environments" / "prod").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "config" / "environments" / "staging").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "json" / "flat").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "empty").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "mixed").mkdir(parents=True, exist_ok=True)

    generate_text_files(BASE_DIR / "small_texts")
    generate_log_files(BASE_DIR / "logs")
    generate_yaml_files(BASE_DIR / "config")
    generate_yaml_files(BASE_DIR / "config" / "environments" / "dev", 10)
    generate_yaml_files(BASE_DIR / "config" / "environments" / "prod", 10)
    generate_yaml_files(BASE_DIR / "config" / "environments" / "staging", 10)
    generate_json_files(BASE_DIR / "json" / "flat")
    generate_text_files(BASE_DIR / "mixed", 5)
    generate_yaml_files(BASE_DIR / "mixed", 5)
    generate_json_files(BASE_DIR / "mixed", 5)

if __name__ == "__main__":
    setup_structure()
    print("Test directory structure and files generated.")
