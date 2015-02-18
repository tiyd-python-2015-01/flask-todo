import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash


DATABASE = '/tmp/to_do.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app=Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return render_template("checklist_add.html")

@app.route("/checklist_results", methods=["POST"])
def add_to_list():
    result = (request.form['item'])
    return render_template("checklist_results.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
