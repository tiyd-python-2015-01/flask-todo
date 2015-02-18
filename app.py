import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

DATABASE = '/tmp/todo.db'
DEBUG = True

app = Flask(__name__)
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

@app.route('/')
def show_entries():
   cur = g.db.execute('select id, title from entries order by id desc')
   entries = [(row[0],row[1]) for row in cur.fetchall()]
   return render_template('layout.html', entries=entries)

@app.route('/', methods=['POST'])
def add_entry():
    task = request.form['title']
    g.db.execute('insert into entries (title) values (?)',
                 (task,))
    g.db.commit()
    return redirect(url_for('show_entries'))

@app.route('/remove', methods=['POST'])
def remove_entry():
    for checked in request.form.getlist('entry'):
        g.db.execute('delete from entries where id = ?', checked)
    g.db.commit()
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
