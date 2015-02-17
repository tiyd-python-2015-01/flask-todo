import sqlite3
from flask import Flask, request, session, g, redirect
from flask import url_for, abort, render_template, flash
from contextlib import closing

DATABASE = '/tmp/todo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def show_entries():
    cur = g.db.execute('select text from entries order by id desc')
    entries = [row[0] for row in cur.fetchall()]
    return entries

def add_entry(new_todo):
    if len(new_todo > 1):
        g.db.execute('insert into entries (text) values (?)',
                     [new_todo])
        g.db.commit()
        flash('New todo added')
    return show_entries()

def delete_entry(todo_togo):
    print("Index = {}".format(todo_togo))

    g.db.execute('delete from entries where (text) = (?)',
                  [todo_togo])
    g.db.commit()
    return show_entries()


@app.route("/", methods=['GET','POST'])
def form():
    if request.method == 'GET':
        entries = show_entries()
        return render_template('todo.html', entries=entries)
    elif request.method == 'POST':
        print(request.form)
        if request.form['input']:
            entries = add_entry(request.form['input'])
        elif request.form['delete']:
            entries = delete_entry(request.form['delete'])
        return render_template('todo.html', entries=entries)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
