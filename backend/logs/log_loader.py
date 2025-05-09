from backend.logs.parser import detect_log_type, parse_log_line
from backend.database.db_connector import insert_log_entry
from backend.logs.error_logger import log_error

def load_log(filepath):
    total, valid, discarded = 0, 0, 0
    with open(filepath, "r") as file:
        log_type = detect_log_type(file)
        file.seek(0)  # Reset pointer

        for line_num, line in enumerate(file, 1):
            total += 1
            parsed = parse_log_line(line.strip(), log_type)
            if parsed:
                insert_log_entry(parsed)
                valid += 1
            else:
                discarded += 1
                log_error(line_num, line.strip(), "Invalid format")

    return {"total": total, "valid": valid, "discarded": discarded}
