import json
import re
from pathlib import Path
from collections import Counter

LOG_LINE_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) '
    r'(?P<level>INFO|WARN|ERROR|DEBUG) '
    r'\[(?P<thread>[^\]]+)\] '
    r'\[(?P<module>[^\]]+)\] '
    r'(?P<message>.+)$'
)

# Serialize log line into structured dict
def parse_log_line(line: str) -> dict:
    match = LOG_LINE_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

# Filter log lines by level and return structured data 
def preprocess_log_file(file_path: str, levels=("Failed", "WARN", "ERROR")) -> list[dict]:
    results = []
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with path.open( 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed and parsed['level'] in levels:
                results.append(parsed)
    return results

# Extract Error, remove repetitive errors, count occurrences
def extract_errors(file_path: str) -> dict:
    errors = preprocess_log_file(file_path, levels=("ERROR",))
    if not errors:
        return {"unique_errors": [], "counts": {}}
    
    msg_counter = Counter()
    first_occurrence = {}  
    for e in errors:
        msg = e["message"]
        msg_counter[msg] += 1
        if msg not in first_occurrence:
            first_occurrence[msg] = {
                "timestamp": e.get("timestamp", ""),
                "module": e.get("module", ""),
                "thread": e.get("thread", "")
            }
        
    unique_errors = []
    for msg, count in msg_counter.items():
        info = first_occurrence[msg]
        unique_errors.append({
            "count": count,
            "timestamp": info["timestamp"],
            "module": info["module"],
            "thread": info["thread"],
            "message": msg
        })

    return {"unique_errors": unique_errors, "counts": dict(msg_counter)}

def save_to_json(data: list, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
