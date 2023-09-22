from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db
from app import app
 
@app.route("/", methods=["GET", "POST"])
def index():
    if len(session) != 0:
        return redirect("/topics")

    return render_template("frontpage.html")


# log in to the application
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT * FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    admin = user[-1]

    if user:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session["username"] = username
            session["admin"] = admin
            return redirect("/topics")
        app.logger.info("väärä salasana")
        return redirect("/")
    
    app.logger.info("käyttäjää ei löydy")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["admin"]
    return redirect("/")


@app.route("/createuser", methods=["POST"])
def createuser():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text(
        "INSERT INTO users (username, password, admin) VALUES (:username, :password, 'FALSE')"
    )
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    return redirect("/")


@app.route("/topics", methods=["GET", "POST"])
def topics():
    sql = text("SELECT * FROM topics ORDER BY name")
    result = db.session.execute(sql)
    topics = result.fetchall()

    sql = text("SELECT * FROM discussions")
    result = db.session.execute(sql)
    discussions = result.fetchall()

    return render_template("topics.html", topics=topics, discussions=discussions)


@app.route("/newtopic", methods=["GET", "POST"])
def newtopic():
    if len(session) == 0:
        return redirect("/")
    if not session["admin"]:
        return redirect("/topics")
    
    return render_template("newtopic.html")

@app.route("/posttopic", methods=["POST"])
def posttopic():
    topic = request.form["topic"]

    sql = text("INSERT INTO topics (name, lastactivity) VALUES (:name, NOW())")
    db.session.execute(sql, {"name": topic})
    db.session.commit()

    return redirect("/topics")

# render the discussions
@app.route("/forum/<int:id>", methods=["GET", "POST"])
def forum(id):
    if len(session) == 0:
        return redirect("/")

    sql = text("SELECT name, id FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    topic = result.fetchone()
    topic_name = topic[0]
    topic_id = topic[1]

    sql = text("SELECT * FROM discussions WHERE topic=:topic")
    result = db.session.execute(sql, {"topic": topic_name})
    discussions = result.fetchall()

    sql = text("SELECT * FROM comments")
    result = db.session.execute(sql)
    comments = result.fetchall()

    sql = text("SELECT * FROM users")
    result = db.session.execute(sql)
    users = result.fetchall()

    logged_user = session["username"]

    return render_template(
        "forum.html",
        discussions=discussions,
        comments=comments,
        users=users,
        logged_user=logged_user,
        topic_name=topic_name,
        topic_id=topic_id,
    )


# add a new discussion
@app.route("/newdiscussion/<int:id>", methods=["GET", "POST"])
def new(id):
    sql = text("SELECT id FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return_id = result.fetchone()[0]

    sql = text("SELECT name FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    topic = result.fetchone()[0]

    return render_template("newdiscussion.html", return_id=return_id, topic=topic)

@app.route("/postdiscussion/<int:id>", methods=["POST"])
def postdiscussion(id):
    """Save a new discussion to database"""

    sql = text("SELECT name FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    topic = result.fetchone()[0]

    title = request.form["title"]
    comment = request.form["comment"]
    username = session["username"]

    sql = text("SELECT id FROM users where username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()[0]

    sql = text("UPDATE topics SET lastactivity=NOW() WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

    sql = text("""INSERT INTO discussions (topic, comment, creator_id, title, time) 
               VALUES (:topic, :comment, :creator_id, :title, NOW())""")
    db.session.execute(
        sql, {"topic": topic, "comment": comment, "creator_id": user, "title": title}
    )
    db.session.commit()

    return redirect(url_for("forum", id=id))


@app.route("/updatediscussion/<int:id>", methods=["GET", "POST"])
def updatediscussion(id):
    """Update a discussion"""

    sql = text("SELECT topic FROM discussions where id=:id")
    result = db.session.execute(sql, {"id": id})
    discussion_topic = result.fetchone()[0]

    sql = text("SELECT id FROM topics WHERE name=:name")
    result = db.session.execute(sql, {"name": discussion_topic})
    topic_id = result.fetchone()[0]

    return render_template("updatediscussion.html", discussion_id=id, topic_id=topic_id)


@app.route("/postdiscussionupdate/<int:id>", methods=["GET", "POST"])
def postdiscussionupdate(id):
    """Save an updated discussion to database"""

    sql = text("SELECT topic FROM discussions WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    discussion_topic = result.fetchone()[0]

    sql = text("SELECT id FROM topics WHERE name=:name")
    result = db.session.execute(sql, {"name": discussion_topic})
    topic_id = result.fetchone()[0]

    title = request.form["title"]
    comment = request.form["comment"]

    if len(comment) == 0:
        return redirect(url_for("updatediscussion", id=id))

    if len(title) == 0:
        sql = text("UPDATE discussions SET comment=:comment WHERE id=:id")
        db.session.execute(sql, {"comment": comment, "id": id})
        db.session.commit()
    else:
        sql = text("UPDATE discussions SET comment=:comment, title=:title WHERE id=:id")
        db.session.execute(sql, {"comment": comment, "title": title, "id": id})
        db.session.commit()

    return redirect(url_for("forum", id=topic_id))

@app.route("/remove/<int:id>")
def remove(id):
    """Remove a discussion"""

    sql = text("DELETE FROM discussions WHERE id=:id RETURNING topic")
    result = db.session.execute(sql, {"id": id})
    discussion_topic = result.fetchone()[0]
    db.session.commit()

    sql = text("SELECT id FROM topics WHERE name=:name")
    result = db.session.execute(sql, {"name": discussion_topic})
    return_id = result.fetchone()[0]

    return redirect(url_for("forum", id=return_id))


@app.route("/removecomment/<int:id>")
def removecomment(id):
    sql = text("DELETE FROM comments WHERE id=:id RETURNING discussion_id")
    result = db.session.execute(sql, {"id": id})
    discussion = result.fetchone()[0]
    db.session.commit()

    return redirect(url_for("addcomment", id=discussion))

@app.route("/removetopic/<int:id>")
def removetopic(id):
    if len(session) == 0:
        return redirect("/")
    if not session["admin"]:
        return redirect("/topics")

    sql = text("DELETE FROM topics WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

    return redirect("/topics")


@app.route("/addcomment/<int:id>", methods=["GET", "POST"])
def addcomment(id):
    sql = text("SELECT * FROM discussions WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    discussion = result.fetchone()

    sql = text("SELECT * FROM comments WHERE discussion_id=:id")
    result = db.session.execute(sql, {"id": id})
    comments = result.fetchall()

    sql = text("SELECT id, username, admin FROM users")
    result = db.session.execute(sql)
    users = result.fetchall()

    logged_user = session["username"]

    return render_template(
        "addcomment.html",
        discussion=discussion,
        comments=comments,
        users=users,
        logged_user=logged_user,
        return_id=discussion[3],
    )


@app.route("/postcomment/<int:id>", methods=["POST"])
def postcomment(id):
    content = request.form["content"]
    username = session["username"]

    sql = text("SELECT id, username FROM users where username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    sql = text(
        """INSERT INTO comments (discussion_id, content, creator_id, creator_name, time)
        VALUES (:id, :content, :creator_id, :creator_name, NOW())"""
    )
    db.session.execute(
        sql,
        {"content": content, "id": id, "creator_id": user[0], "creator_name": user[1]},
    )
    db.session.commit()
    return redirect(url_for("addcomment", id=id))


@app.route("/search", methods=["POST"])
def search():
    content = request.form["content"]

    sql = text(
        "SELECT * FROM discussions WHERE comment LIKE :content OR title LIKE :content"
    )
    result = db.session.execute(sql, {"content": "%" + content + "%"})
    discussions = result.fetchall()

    sql = text("SELECT * FROM discussions")
    result = db.session.execute(sql)
    all_discussions = result.fetchall()

    sql = text("SELECT * FROM comments WHERE content LIKE :content")
    result = db.session.execute(sql, {"content": "%" + content + "%"})
    comments = result.fetchall()

    return render_template(
        "search.html",
        discussions=discussions,
        comments=comments,
        all_discussions=all_discussions,
        content=content,
    )
