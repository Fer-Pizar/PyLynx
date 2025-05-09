from sqlalchemy import Column, Integer, String, DateTime
from backend.database.db_config import Base

class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    ip = Column(String)
    timestamp = Column(String)  # Convert to DateTime if needed
    method = Column(String, nullable=True)
    resource = Column(String, nullable=True)
    status = Column(Integer, nullable=True)
    action = Column(String, nullable=True)
    file = Column(String, nullable=True)
    user = Column(String, nullable=True)
