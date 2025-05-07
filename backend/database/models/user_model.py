from sqlalchemy import Column, Integer, String, Enum
from backend.database.db_config import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum('admin', 'viewer', name='user_roles'), nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
