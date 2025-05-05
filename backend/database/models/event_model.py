from sqlalchemy import Column, Integer, String, DateTime
from backend.database.db_config import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    ip = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    service = Column(String, nullable=False)
    message = Column(String, nullable=False)
