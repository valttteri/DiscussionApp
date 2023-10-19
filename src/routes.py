"""Import libraries"""
from flask import redirect, render_template, request, session, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db
from app import app
import tools

@app.route("/", methods=["GET", "POST"])
def index():
    """Front page"""
    sql = text("SELECT * FROM discussions ORDER BY time DESC")
    result = db.session.execute(sql)
    discussions = result.fetchall()

    users = tools.get_all('users')
    topics = tools.get_all('topics')
    comments = tools.get_all('comments')

    if discussions:
        return render_template(
            "frontpage.html",
            discussions=discussions,
            users=users,
            topics=topics,
            comments=comments
        )
    return render_template("frontpage.html")

@app.route("/closeflash/<int:id>", methods=["GET"])
def closeflash(id):
    """When user closes a notification message, the app redirects the user.
    This function determines the redirecting address"""
    session.pop('flashes', None)
    address = [
        "not in use",
        "/createuser",
        "/",
        "/topics",
        "/privatetopics",
        "/newtopic"
    ]

    return redirect(address[id])

@app.route("/loggingin", methods=["GET", "POST"])
def loggingin():
    """Render the login page"""
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """This function is called when a user attempts to log in"""
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT * FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        flash("Virheellinen käyttäjänimi")
        return redirect("/")

    user_id = user[0]
    admin = user[-1]
    password_hash = user.password

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        session["admin"] = admin
        flash(f"Kirjauduttu sisään käyttäjällä {username}")
        return redirect("/")
    flash("Virheellinen salasana")
    return redirect("/")

@app.route("/logout")
def logout():
    """Log out a user"""
    username = session["username"]
    flash(f"Kirjattiin ulos käyttäjä {username}")
    del session["username"]
    del session["admin"]
    del session["user_id"]
    return redirect("/")

@app.route("/createuser", methods=["GET", "POST"])
def createuser():
    """Render the registration page"""
    return render_template("createaccount.html")

@app.route("/savenewuser", methods=["GET", "POST"])
def savenewuser():
    """Save a new user to the database, if input is valid"""
    username = request.form["username"]
    is_admin = request.form.getlist("admin")

    if tools.bad_username(username):
        return redirect("/createuser")

    password = request.form["password"]

    if tools.bad_password(password):
        return redirect("/createuser")

    hash_value = generate_password_hash(password)

    if is_admin:
        sql = text(
            "INSERT INTO users (username, password, admin) VALUES (:username, :password, 'TRUE')"
        )
    else:
        sql = text(
            "INSERT INTO users (username, password, admin) VALUES (:username, :password, 'FALSE')"
        )
    flash("Luotiin uusi käyttäjä")
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    return redirect("/")


@app.route("/topics", methods=["GET", "POST"])
def topicpage():
    """Render the discussion channels"""
    sql = text("SELECT * FROM topics ORDER BY name")
    result = db.session.execute(sql)
    topics = result.fetchall()

    discussions = tools.get_all('discussions')

    return render_template("topics.html", topics=topics, discussions=discussions)


@app.route("/newtopic", methods=["GET", "POST"])
def newtopic():
    """Render the page for creating a new discussion channel"""
    return render_template("newtopic.html")

@app.route("/posttopic", methods=["POST"])
def posttopic():
    """Save a new discussion channel to the database, if input is valid"""
    if len(session) == 0:
        flash("Kirjaudu sisään luodaksesi kanavan")
        return redirect("/")
    topic = request.form["topic"]

    if tools.invalid_topic(topic):
        return redirect("/newtopic")

    sql = text("INSERT INTO topics (name, lastactivity) VALUES (:name, NOW())")
    db.session.execute(sql, {"name": topic})
    db.session.commit()
    flash(f"Luotiin kanava {topic}")
    return redirect("/topics")

@app.route("/forum/<int:id>", methods=["GET", "POST"])
def forum(id):
    """Render the discussions of a specific topic"""
    sql = text("SELECT name, id FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id}).fetchone()
    topic_name = result[0]
    topic_id = result[1]

    sql = text("SELECT * FROM discussions WHERE topic=:topic")
    result = db.session.execute(sql, {"topic": topic_name})
    discussions = result.fetchall()

    comments = tools.get_all('comments')

    users = tools.get_all('users')

    return render_template(
        "forum.html",
        discussions=discussions,
        comments=comments,
        users=users,
        topic_name=topic_name,
        topic_id=topic_id,
    )

@app.route("/newdiscussion/<int:id>", methods=["GET", "POST"])
def newdiscussion(id):
    """Create a new discussion"""
    if len(session) == 0:
        flash("Kirjaudu sisään lisätäksesi uuden keskustelun")
        return redirect("/topics")

    sql = text("SELECT DISTINCT id, name FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id}).fetchone()

    return_id = result[0]
    topic = result[1]

    return render_template("newdiscussion.html", return_id=return_id, topic=topic)

@app.route("/postdiscussion/<int:id>", methods=["POST"])
def postdiscussion(id):
    """Save a new discussion to database"""
    if len(session) == 0:
        return redirect("/")

    sql = text("SELECT name FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    topic = result.fetchone()[0]

    title = request.form["title"]
    comment = request.form["comment"]
    username = session["username"]

    if not username:
        return redirect("/")
    if not tools.valid_discussion(title, comment):
        return redirect("/topics")

    sql = text("SELECT id FROM users where username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()[0]

    sql = text("UPDATE topics SET lastactivity=NOW() WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

    sql = text("""INSERT INTO discussions (topic, comment, creator_id, title, time) 
               VALUES (:topic, :comment, :creator_id, :title, NOW())""")
    db.session.execute(
        sql, {
            "topic": topic,
            "comment": comment,
            "creator_id": user,
            "title": title
        }
    )
    db.session.commit()

    return redirect(url_for("forum", id=id))


@app.route("/updatediscussion/<int:id>", methods=["GET", "POST"])
def updatediscussion(id):
    """Update a discussion"""
    if len(session) == 0:
        return redirect("/")

    sql = text("SELECT * FROM discussions where id=:id")
    result = db.session.execute(sql, {"id": id})
    discussion = result.fetchone()
    discussion_topic = discussion[1]
    discussion_creator = discussion[3]

    user_id = session["user_id"]
    is_admin = session["admin"]
    if discussion_creator != user_id and not is_admin:
        return redirect("/")

    sql = text("SELECT id FROM topics WHERE name=:name")
    result = db.session.execute(sql, {"name": discussion_topic})
    topic_id = result.fetchone()[0]

    return render_template(
        "updatediscussion.html",
        discussion_id=id,
        topic_id=topic_id,
        discussion=discussion
    )


@app.route("/postdiscussionupdate/<int:id>", methods=["GET", "POST"])
def postdiscussionupdate(id):
    """Save an updated discussion to database"""
    if len(session) == 0:
        return redirect("/")

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

    return redirect(url_for("addcomment", id=id))

@app.route("/remove/<int:id>")
def removediscussion(id):
    """Remove a discussion"""
    if len(session) == 0:
        return redirect("/")
    
    user_id = session["user_id"]
    is_admin = session["admin"]

    sql = text("SELECT title from discussions WHERE id=:id AND creator_id=:user_id")
    result = db.session.execute(sql, {"id": id, "user_id": user_id}).fetchone()

    if not result and not is_admin:
        return redirect("/")

    sql = text("DELETE FROM discussions WHERE id=:id RETURNING topic")
    db.session.execute(sql, {"id": id})
    db.session.commit()

    flash("Keskustelu poistettu")
    return redirect("/")

@app.route("/removecomment/<int:id>")
def removecomment(id):
    """Remove a comment"""
    if len(session) == 0:
        return redirect("/")

    sql = text("DELETE FROM comments WHERE id=:id RETURNING discussion_id")
    result = db.session.execute(sql, {"id": id})
    discussion = result.fetchone()[0]
    db.session.commit()

    return redirect(url_for("addcomment", id=discussion))

@app.route("/removetopic/<int:id>")
def removetopic(id):
    """Remove a topic"""
    if len(session) == 0:
        return redirect("/")
    if not session["admin"]:
        return redirect("/topics")

    sql = text("DELETE FROM topics WHERE id=:id RETURNING name")
    result = db.session.execute(sql, {"id": id}).fetchone()
    topic = result[0]
    db.session.commit()
    flash(f"Kanava {topic} poistettu")
    return redirect("/topics")

@app.route("/addcomment/<int:id>", methods=["GET", "POST"])
def addcomment(id):
    """Render a certain discussion"""
    sql = text("SELECT DISTINCT * FROM discussions WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    discussion = result.fetchone()

    sql = text("SELECT DISTINCT id FROM topics WHERE name=:name")
    result = db.session.execute(sql, {"name": discussion[1]})
    return_id = result.fetchone()[0]

    sql = text("SELECT * FROM comments WHERE discussion_id=:id")
    result = db.session.execute(sql, {"id": id})
    comments = result.fetchall()

    sql = text("SELECT DISTINCT id, username, admin FROM users")
    result = db.session.execute(sql)
    users = result.fetchall()

    if len(session) > 0:
        logged_user = session["username"]
    else:
        logged_user = None

    return render_template(
        "addcomment.html",
        discussion=discussion,
        comments=comments,
        users=users,
        logged_user=logged_user,
        return_id=return_id,
    )


@app.route("/postcomment/<int:id>", methods=["POST"])
def postcomment(id):
    """Save a new comment"""
    if len(session) == 0:
        flash("Kirjaudu sisään kommentoidaksesi")
        return redirect("/")

    content = request.form["content"]
    username = session["username"]

    if len(content) == 0:
        return redirect(url_for("addcomment", id=id))
    if len(content) > 300:
        flash("Comment can't be longer than 300 characters")
        return redirect("/topics")

    sql = text("SELECT DISTINCT id, username FROM users where username=:username")
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
    """Render search results"""
    content = request.form["content"]

    sql = text(
        "SELECT * FROM discussions WHERE comment LIKE :content OR title LIKE :content"
    )
    result = db.session.execute(sql, {"content": "%" + content + "%"})
    discussions = result.fetchall()

    all_discussions = tools.get_all("discussions")

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

@app.route("/privatetopics", methods=["GET", "POST"])
def privatetopics():
    """Render group chats"""
    if len(session) == 0:
        flash("Kirjaudu sisään nähdäksesi omat keskustelut")
        return redirect("/")

    logged_user_id = session["user_id"]

    sql = text(
        """SELECT d.id, d.title, d.creator_id FROM private_discussions d JOIN private_rights r
            ON d.id=r.discussion_id AND r.user_id=:logged_user_id"""
    )
    result = db.session.execute(sql, {"logged_user_id": logged_user_id})
    private_discussions = result.fetchall()

    sql = text("SELECT * FROM private_comments ORDER BY time DESC")
    result = db.session.execute(sql)
    private_comments = result.fetchall()

    return render_template(
        "privatetopics.html",
        private_discussions=private_discussions,
        private_comments=private_comments
    )

@app.route("/newprivatetopic", methods=["GET", "POST"])
def newprivatetopic():
    """Create a new group chat"""
    if len(session) == 0:
        return redirect("/")

    logged_user = session["user_id"]

    sql = text("SELECT DISTINCT * FROM users WHERE id!=:logged_user")
    result = db.session.execute(sql, {"logged_user": logged_user})
    users = result.fetchall()

    return render_template("newprivatetopic.html", users=users)

@app.route("/postprivatetopic", methods=["GET", "POST"])
def postprivatetopic():
    """Save a group chat to database, if input is valid"""
    if len(session) == 0:
        return redirect("/")

    title = request.form["title"]
    members = request.form.getlist("member")
    user_id = session["user_id"]

    if not members:
        flash("Valitse keskusteluun ainakin yksi jäsen")
        return redirect("/privatetopics")
    if len(title) == 0:
        flash("Valitse keskustelulle nimi")
        return redirect("/privatetopics")
    if len(title) > 50:
        flash("Keskustelun nimi voi olla enintään 50 merkkiä pitkä")
        return redirect("/privatetopics")

    sql = text(
        """INSERT INTO private_discussions (title, creator_id, lastactivity)
        VALUES (:title, :creator_id, NOW()) RETURNING id"""
    )
    flash("Uusi keskustelu lisätty")
    result = db.session.execute(sql, {"title": title, "creator_id": user_id})
    discussion_id = result.fetchone()[0]
    db.session.commit()

    sql = text(
        """INSERT INTO private_rights (user_id, discussion_id)
        VALUES (:user_id, :discussion_id)"""
    )
    db.session.execute(sql, {"user_id": user_id, "discussion_id": discussion_id})
    db.session.commit()

    for member in members:
        sql = text(
        """INSERT INTO private_rights (user_id, discussion_id)
        VALUES (:user_id, :discussion_id)"""
        )
        db.session.execute(sql, {"user_id": member, "discussion_id": discussion_id})
        db.session.commit()

    return redirect("/privatetopics")

@app.route("/removeprivatetopic/<int:id>")
def removeprivatetopic(id):
    """Remove a groupchat"""
    if len(session) == 0:
        return redirect("/")

    sql = text("DELETE FROM private_discussions WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

    return redirect("/privatetopics")

@app.route("/groupchat/<int:id>", methods=["GET"])
def groupchat(id):
    """Render a certain groupchat"""
    if len(session) == 0:
        return redirect("/")
    
    user_id = session["user_id"]

    sql = text("""SELECT d.id from private_discussions d, private_rights r
               where d.id=:id and r.user_id=:user_id""")
    result = db.session.execute(sql, {"id": id, "user_id": user_id}).fetchone()
    if not result:
        return redirect("/")

    sql = text("SELECT * FROM private_discussions WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    chat = result.fetchone()

    sql = text("SELECT * FROM private_comments WHERE discussion_id=:id ORDER BY time DESC")
    result = db.session.execute(sql, {"id": id})
    comments = result.fetchall()

    sql = text("""SELECT u.id, u.username, u.admin FROM users u JOIN private_rights r
               ON u.id=r.user_id AND r.discussion_id=:chat_id""")
    result = db.session.execute(sql, {"chat_id":id})
    users = result.fetchall()

    sql = text("""SELECT COUNT(*) FROM users u JOIN private_rights r
               ON u.id=r.user_id AND r.discussion_id=:chat_id""")
    result = db.session.execute(sql, {"chat_id":id})
    user_count = result.fetchone()[0]

    return render_template(
        "groupchat.html",
        chat=chat,
        comments=comments,
        users=users,
        user_count=user_count
    )

@app.route("/addprivatecomment/<int:id>", methods=["POST"])
def addprivatecomment(id):
    """Send a message to a group chat"""
    if len(session) == 0:
        return redirect("/")

    content = request.form["content"]
    username = session["username"]

    sql = text("SELECT id, username FROM users where username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    sql = text(
        """INSERT INTO private_comments (content, discussion_id, creator_id, creator_name, time)
        VALUES (:content, :discussion_id, :creator_id, :creator_name, NOW())"""
    )
    db.session.execute(
        sql,
        {"content": content, "discussion_id": id, "creator_id": user[0], "creator_name": user[1]},
    )
    db.session.commit()

    sql = text("UPDATE private_discussions SET lastactivity=NOW() WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

    return redirect(url_for("groupchat", id=id))

@app.route("/removeprivatecomment/<int:id>")
def removeprivatecomment(id):
    """Remove a message from a group chat"""
    if len(session) == 0:
        return redirect("/")

    sql = text("DELETE FROM private_comments WHERE id=:id RETURNING discussion_id")
    result = db.session.execute(sql, {"id": id})
    discussion = result.fetchone()[0]
    db.session.commit()

    return redirect(url_for("groupchat", id=discussion))

@app.route("/info")
def info():
    """Render the info page"""

    sql = text("SELECT COUNT(*) FROM comments")
    total_comments = db.session.execute(sql).fetchone()[0]

    sql = text("SELECT COUNT(*) FROM discussions")
    total_discussions = db.session.execute(sql).fetchone()[0]

    sql = text("SELECT COUNT(*) FROM topics")
    total_topics = db.session.execute(sql).fetchone()[0]

    sql = text("SELECT COUNT(*) FROM users")
    total_users = db.session.execute(sql).fetchone()[0]

    sql = text("""SELECT discussion_id, COUNT(*) from comments GROUP BY discussion_id
               ORDER BY COUNT(*) DESC""")
    result = db.session.execute(sql).fetchone()
    most_commented_id = result[0]
    comment_count = result[1]
    
    sql = text("SELECT * from discussions where id=:id")
    top_discussion = db.session.execute(sql, {"id": most_commented_id}).fetchone()

    users = tools.get_all("users")

    return render_template(
        "info.html",
        total_comments=total_comments,
        total_discussions=total_discussions,
        total_topics=total_topics,
        total_users=total_users,
        top_discussion=top_discussion,
        users=users,
        comment_count = comment_count
    )
