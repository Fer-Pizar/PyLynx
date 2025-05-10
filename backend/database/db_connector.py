from backend.database.models.log_entry import LogEntry
from backend.database.db_config import Session


def insert_log_entry(log_dict):
    db = Session()
    try:
        entry = LogEntry(**log_dict)
        db.add(entry)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting log: {e}")
    finally:
        db.close()

def insert_log_entry(data, log_type):
    """
    Simulates database insert. In production, replace with real DB logic.
    """
    print(f"[DB] Inserting {log_type.upper()} log: {data}")
