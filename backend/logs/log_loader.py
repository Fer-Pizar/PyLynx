import re
from backend.logs.parser import parse_apache_line, parse_ftp_line
from backend.logs.error_logger import log_error
from backend.database.db_connector import insert_log_entry

def detect_log_type(line):
    """
    Detects the type of log based on line content.
    Returns 'apache' or 'ftp' or None.
    """
    if re.search(r'^\d{1,3}(\.\d{1,3}){3}', line):  # Apache logs start with IP
        return 'apache'
    elif re.search(r'USER|RETR|STOR|230|530', line):  # Common FTP commands
        return 'ftp'
    return None

def load_log_file(filepath):
    total = 0
    valid = 0
    invalid = 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_number, line in enumerate(f, start=1):
                total += 1
                line = line.strip()
                if not line:
                    log_error(line_number, line, "Empty line")
                    invalid += 1
                    continue

                log_type = detect_log_type(line)
                if not log_type:
                    log_error(line_number, "Unknown log type")
                    invalid += 1
                    continue

                parsed_data = None
                if log_type == 'apache':
                    parsed_data = parse_apache_line(line)
                elif log_type == 'ftp':
                    parsed_data = parse_ftp_line(line)

                if parsed_data:
                    insert_log_entry(parsed_data, log_type)
                    valid += 1
                else:
                    log_error(line_number, "Failed to parse line")
                    invalid += 1

        return {
            "total_lines": total,
            "valid_lines": valid,
            "invalid_lines": invalid
        }

    except FileNotFoundError:
        return {"error": "File not found"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
