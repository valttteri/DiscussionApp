"""Import modules"""
from sqlalchemy.sql import text
from flask import flash
from db import db

def bad_username(username: str):
    """Check if a username is taken while creating a new account"""
    sql = text("SELECT username from users where username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        flash("Tämä käyttäjänimi on jo käytössä")
        return True
    if len(username) < 5 or len(username) > 20:
        flash("Käyttäjänimen on oltava 5-20 merkin pituinen")
        return True

    return False


def bad_password(password: str):
    """Check if a new password is good enough"""

    if len(password) < 8:
        flash("Salasanan on oltava vähintään 5 merkkiä pitkä")
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
    """Return all rows from a table"""
    sql = text(f"SELECT * FROM {table_name}")
    result = db.session.execute(sql)
    objects = result.fetchall()
    return objects

def get_all_conditional(table_name: str, column: str, value):
    """Return all rows with a condition"""
    sql = text(f"SELECT * FROM {table_name} WHERE {column}=:{value}")
    result = db.session.execute(sql, {f"{value}": value})
    objects = result.fetchone()
    return objects

def invalid_topic(topic: str):
    """Check if a new discussion channel name is valid"""
    if len(topic) < 3 or len(topic) > 30:
        flash("Kanavan nimen on oltava 3-30 merkin pituinen")
        return True

    sql = text("SELECT * FROM topics WHERE name=:name")
    result = db.session.execute(sql, {"name": topic}).fetchone()
    if result:
        flash(f"Kanava {topic} on jo olemassa")
        return True
    return False
