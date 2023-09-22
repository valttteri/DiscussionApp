from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

url = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = url
db = SQLAlchemy(app)
