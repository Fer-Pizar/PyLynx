from backend.database.models.log_entry import LogEntry
from backend.database.db_config import SessionLocal

def insert_log_entry(log_dict):
    db = SessionLocal()
    try:
        entry = LogEntry(**log_dict)
        db.add(entry)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting log: {e}")
    finally:
        db.close()
