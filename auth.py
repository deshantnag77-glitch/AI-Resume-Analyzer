"""
auth.py
-------
Handles user registration, login and validation logic.
Passwords are hashed with bcrypt — never stored in plain text.
"""

import re
import bcrypt
import database as db


class AuthError(Exception):
    pass


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email.strip()) is not None


def is_valid_password(password: str) -> tuple:
    """
    Returns (is_valid, message).
    Minimum practical strength: 8+ chars, at least one letter and one number.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, ""


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def register_user(name: str, email: str, password: str, confirm_password: str) -> dict:
    name = name.strip()
    email = email.strip()

    if not name:
        raise AuthError("Full name is required.")

    if not is_valid_email(email):
        raise AuthError("Please enter a valid email address.")

    if password != confirm_password:
        raise AuthError("Passwords do not match.")

    valid, message = is_valid_password(password)
    if not valid:
        raise AuthError(message)

    if db.get_user_by_email(email):
        raise AuthError("An account with this email already exists.")

    password_hash = hash_password(password)
    user_id = db.create_user(name, email, password_hash)
    return db.get_user_by_id(user_id)


def login_user(email: str, password: str) -> dict:
    email = email.strip()
    user = db.get_user_by_email(email)

    if not user:
        raise AuthError("No account found with this email.")

    if not verify_password(password, user["password_hash"]):
        raise AuthError("Incorrect password.")

    return user
