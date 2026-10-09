"""Log parsing helper: simple CLI to extract timestamps, levels and messages from log files."""

import re
import sys
from pathlib import Path

def parse_log_line(line):
    ts_match = re.search(r'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:,\d{3})?', line)
    if not ts_match:
        return None
    ts = ts_match.group(0)
    level_match = re.search(r'\b(INFO|ERROR|DEBUG|WARNING|CRITICAL)\b', line)
    level = level_match.group(0) if level_match else None
    idx = level_match.end() if level_match else 0
    message = line[idx:].strip()
    return ts, level, message

def parse_file(path):
    for line in Path(path).read_text().splitlines():
        res = parse_log_line(line)
        if res:
            print(f'{res[0]} | {res[1] or "N/A"} | {res[2]}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <logfile>')
        sys.exit(1)
    parse_file(sys.argv[1])