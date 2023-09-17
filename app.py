from flask import Flask
from flask import redirect, render_template, request, session, url_for
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
    sql = text("SELECT * FROM discussions")
    result = db.session.execute(sql)
    discussions = result.fetchall()

    sql = text("SELECT * FROM comments")
    result = db.session.execute(sql)
    comments = result.fetchall()

    sql = text("SELECT * FROM users")
    result = db.session.execute(sql)
    users = result.fetchall()

    logged_user = session["username"]

    return render_template("forum.html", discussions=discussions, comments=comments, users=users, logged_user=logged_user)

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

    sql = text("INSERT INTO discussions (topic, comment, creator_id, time) VALUES (:topic, :comment, :creator_id, NOW())")
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
    
    sql = text("DELETE FROM comments WHERE id=:id RETURNING discussion_id")
    result = db.session.execute(sql, {"id":id})
    discussion = result.fetchone()[0]
    print(discussion)
    db.session.commit()

    return redirect(url_for('addcomment', id=discussion))

@app.route("/addcomment/<int:id>", methods=['GET', 'POST'])
def addcomment(id):
    sql = text("SELECT * FROM discussions WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    discussion = result.fetchone()

    sql = text("SELECT * FROM comments WHERE discussion_id=:id")
    result = db.session.execute(sql, {"id":id})
    comments = result.fetchall()

    sql = text("SELECT id, username FROM users")
    result = db.session.execute(sql, {"id":id})
    users = result.fetchall()

    logged_user = session["username"]

    return render_template("addcomment.html", discussion=discussion, comments=comments, users=users, logged_user=logged_user)

@app.route("/postcomment/<int:id>", methods=["POST"])
def postcomment(id):
    content = request.form["content"]
    username = session["username"]

    sql = text("SELECT id FROM users where username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()[0]

    sql = text("INSERT INTO comments (discussion_id, content, creator_id, time) VALUES (:id, :content, :creator_id, NOW())")
    db.session.execute(sql, {"content":content, "id": id, "creator_id":user})
    db.session.commit()
    return redirect(url_for('addcomment', id=id))