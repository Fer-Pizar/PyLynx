from backend.database.db_connector import get_user_by_username
from werkzeug.security import check_password_hash, generate_password_hash

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return check_password_hash(hashed, password)

def login(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        raise ValueError("User not found.")
    if not verify_password(password, user.password_hash):
        raise ValueError("Incorrect password.")
    return user  # return full user object
