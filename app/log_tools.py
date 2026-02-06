import json
import re
from pathlib import Path

LOG_LINE_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) '
    r'(?P<level>INFO|WARN|ERROR|DEBUG) '
    r'\[(?P<thread>[^\]]+)\] '
    r'\[(?P<module>[^\]]+)\] '
    r'(?P<message>.+)$'
)

# 先把log文件解析成json，方便后续分析和处理
def parse_log_line(line: str) -> dict:
    match = LOG_LINE_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

# 以防止log文件过大，导致内存问题，可以考虑分批次读取和处理
def preprocess_log_file(file_path: str, levels=("Failed", "WARN", "ERROR")) -> list:
    results = []
    path = Path(file_path)
    if not path.is_file():
        raise (f"File not found: {file_path}")
        return results
    with path.open( 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed and parsed['level'] in levels:
                results.append(parsed)
    return results

def extract_errors(file_path: str) -> list:
    return preprocess_log_file(file_path, levels=("ERROR"))

def save_to_json(data: list, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



# 1. path import失败，怎么添加
# 2. 第一个parse_log_line函数，正则表达式的匹配规则是什么？是不是针对不同log可以写不同的处理方式？
# 3. 这里的file_path是什么？我们不是打算用upload吗？
# 4. parsed("levels")有什么作用？
# 5. raise 和 print的区别是什么？
# 6. pending，自己多加一个warn + failed

