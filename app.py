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

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    sql = text("SELECT topic, comment FROM discussions")
    result = db.session.execute(sql)
    discussions = result.fetchall()
    return render_template("forum.html", discussions=discussions)

@app.route("/newdiscussion", methods=['GET', 'POST'])
def new():
    return render_template("newdiscussion.html")

@app.route("/postdiscussion", methods=["POST"])
def postdiscussion():
    topic = request.form["topic"]
    comment = request.form["comment"]
    sql = text("INSERT INTO discussions (topic, comment) VALUES (:topic, :comment)")
    db.session.execute(sql, {"topic":topic, "comment":comment})
    db.session.commit()
    return redirect("/forum")
