import re
from datetime import datetime

def parse_apache_line(line):
    """
    Parses an Apache log line.
    Example: 127.0.0.1 - - [10/Oct/2023:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326
    """
    pattern = r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) .* \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<resource>.*?) HTTP.*" (?P<status>\d{3})'
    match = re.match(pattern, line)
    if match:
        return {
            "ip": match.group("ip"),
            "timestamp": parse_datetime(match.group("timestamp")),
            "method": match.group("method"),
            "resource": match.group("resource"),
            "status": int(match.group("status"))
        }
    return None

def parse_ftp_line(line):
    """
    Parses a typical FTP log line.
    Example: Mon Oct 10 14:22:01 2023 [pid 1234] [user] OK LOGIN: Client "192.168.1.2"
    """
    pattern = r'(?P<date>\w+ \w+ \d+ \d+:\d+:\d+ \d+).* \[(?P<user>\w+)\].*Client "(?P<ip>\d{1,3}(?:\.\d{1,3}){3})"'
    match = re.search(pattern, line)
    if match:
        return {
            "timestamp": parse_datetime(match.group("date")),
            "user": match.group("user"),
            "ip": match.group("ip"),
            "action": "LOGIN",  # Simplified for now
            "status": "OK"
        }
    return None

def parse_datetime(dt_str):
    try:
        if '/' in dt_str:
            return datetime.strptime(dt_str, "%d/%b/%Y:%H:%M:%S %z")
        else:
            return datetime.strptime(dt_str, "%a %b %d %H:%M:%S %Y")
    except Exception:
        return None
