from flask import Flask
from flask import render_template, request

app = Flask(__name__)

#etusivu
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('frontpage.html')

#keskustelualueet
@app.route('/forum', methods=['POST', 'GET'])
def page2():
    topic='topologia on kivaa'
    return render_template('forum.html', topic=topic)
