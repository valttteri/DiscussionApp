from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
url =  getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = url
db = SQLAlchemy(app)

#etusivu
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('frontpage.html')

#keskustelualueet
@app.route('/forum', methods=['POST', 'GET'])
def page2():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template('forum.html', messages=messages)

@app.route("/new", methods=['GET', 'POST'])
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/forum")
