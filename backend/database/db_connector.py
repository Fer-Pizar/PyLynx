from backend.database.models.user_model import User
from backend.database.db_config import Session
from backend.security.auth import hash_password

def create_user(username: str, password: str, role: str):
    session = Session()
    try:
        if session.query(User).filter_by(username=username).first():
            raise ValueError("Username already exists.")
        user = User(
            username=username,
            password_hash=hash_password(password),
            role=role
        )
        session.add(user)
        session.commit()
        print(f"✅ User '{username}' created with role '{role}'.")
    finally:
        session.close()

def get_user_by_username(username: str):
    session = Session()
    try:
        return session.query(User).filter_by(username=username).first()
    finally:
        session.close()
