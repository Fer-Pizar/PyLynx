import re

def detect_log_type(file):
    """
    Inspects the first line of the file to determine its type.
    """
    sample = file.readline()
    if "GET" in sample or "POST" in sample:
        return "apache"
    elif "FTP" in sample or "vsftpd" in sample or "RETR" in sample or "STOR" in sample:
        return "ftp"
    return "unknown"

def parse_log_line(line, log_type):
    """
    Parses a single line of a log file based on its type.

    Parameters:
        line (str): The raw log line.
        log_type (str): Either 'apache' or 'ftp'.

    Returns:
        dict | None: Parsed data or None if the line is invalid.
    """
    if log_type == "apache":
        # Example: 127.0.0.1 - - [10/May/2025:13:55:36 +0000] "GET /index.html HTTP/1.1" 200
        match = re.match(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(\w+) (.*?) HTTP.*" (\d+)', line)
        if match:
            return {
                "ip": match.group(1),
                "timestamp": match.group(2),
                "method": match.group(3),
                "resource": match.group(4),
                "status": int(match.group(5)),
                "type": "apache"
            }

    elif log_type == "ftp":
        # Example: RETR file.txt by user1 from 192.168.1.5
        match = re.match(r'(\w+)\s+(.*?)\s+by\s+(.*?)\s+from\s+(\d+\.\d+\.\d+\.\d+)', line)
        if match:
            return {
                "action": match.group(1),
                "file": match.group(2),
                "user": match.group(3),
                "ip": match.group(4),
                "type": "ftp"
            }

    return None
