import os
from datetime import datetime

ERROR_LOG_PATH = "log_errors.txt"

def log_error(line_number, line_content, reason):
    """
    Logs a parsing error with line number and reason to be clearer.


    Parameters:
        line_number (int): The line number in the original log file.
        line_content (str): The raw content of the line that failed to parse.
        reason (str): Explanation of why the line was invalid.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] Line {line_number}: {reason} >> {line_content}\n"

    with open(ERROR_LOG_PATH, "a") as f:
        f.write(log_message)

def clear_error_log():
    """
    Clears the content of the error log (useful for testing or resets).
    """
    if os.path.exists(ERROR_LOG_PATH):
        os.remove(ERROR_LOG_PATH)
