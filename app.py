from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
url =  getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = url
db = SQLAlchemy(app)
app.secret_key = getenv('SECRET_KEY')

#front page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('frontpage.html')

#log in to the application
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 
    
    if user:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/forum")
        else:
            app.logger.info('väärä salasana')
            return redirect("/")
    app.logger.info('käyttäjää ei löydy')
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/createuser", methods=['POST'])
def createuser():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

#render the discussions
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    sql = text("SELECT id, topic, comment, creator_id FROM discussions")
    result = db.session.execute(sql)
    discussions = result.fetchall()

    sql = text("SELECT discussion_id, content FROM comments")
    result = db.session.execute(sql)
    comments = result.fetchall()

    sql = text("SELECT id, username FROM users")
    result = db.session.execute(sql)
    users = result.fetchall()

    return render_template("forum.html", discussions=discussions, comments=comments, users=users)

#add a new discussion
@app.route("/newdiscussion", methods=['GET', 'POST'])
def new():
    return render_template("newdiscussion.html")

#function for saving a new discussion
@app.route("/postdiscussion", methods=["POST"])
def postdiscussion():
    topic = request.form["topic"]
    comment = request.form["comment"]
    username = session["username"]

    sql = text("SELECT id FROM users where username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()[0]
    print(user)

    sql = text("INSERT INTO discussions (topic, comment, creator_id) VALUES (:topic, :comment, :creator_id)")
    db.session.execute(sql, {"topic":topic, "comment":comment, "creator_id":user})
    db.session.commit()

    return redirect("/forum")

#function for removing a discussion
@app.route("/remove/<int:id>")
def remove(id):
    sql = text("DELETE FROM discussions WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect("/forum")

@app.route("/removecomment/<int:id>")
def removecomment(id):
    sql = text("DELETE FROM comments WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect("/forum")

@app.route("/addcomment/<int:id>")
def addcomment(id):
    sql = text("SELECT topic, comment, id FROM discussions WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    discussion = result.fetchone()

    sql = text("SELECT id, content FROM comments WHERE discussion_id=:id")
    result = db.session.execute(sql, {"id":id})
    comments = result.fetchall()

    return render_template("newcomment.html", discussion=discussion, comments=comments)

@app.route("/postcomment/<int:id>", methods=["POST"])
def postcomment(id):
    content = request.form["content"]
    sql = text("INSERT INTO comments (discussion_id, content) VALUES (:id, :content)")
    db.session.execute(sql, {"content":content, "id": id})
    db.session.commit()
    return redirect("/forum")