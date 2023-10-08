from sqlalchemy.sql import text
from flask import flash
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

def valid_discussion(title:str, comment:str):
    """Check if user is trying to post a valid discussion"""
    if len(title) == 0:
        flash("Valitse otsikko")
        return False
    if len(comment) == 0:
        flash("Kirjoita keskustelulle avaus")
        return False
    if len(title) > 50:
        flash("Otsikko ei saa olla 50 merkkiä pidempi")
        return False
    if len(comment) > 300:
        flash("Avaus ei voi olla 300 merkkiä pidempi")
        return False

    return True

def get_all(table_name: str):
    """Return all objects from a table"""
    sql = text(f"SELECT * FROM {table_name}")
    result = db.session.execute(sql)
    objects = result.fetchall()
    return objects