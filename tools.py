from sqlalchemy.sql import text
from db import db

def username_taken(username: str):
    """Check if a username is taken while creating a new account"""
    sql = text("SELECT username from users where username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False
    return True

def bad_password(password: str):
    """Check if a new password is good enough"""

    if len(password) < 5:
        return True
    return False
