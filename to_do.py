import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'joel'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('todo_schema.sql', mode='r') as f:
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
def show_list():
    cur = g.db.execute('select task from entries order by id desc')
    entries = [row[0] for row in cur.fetchall()]
    return render_template('show_list.html', entries=entries)


@app.route('/', methods=['POST'])
def add_task():
    g.db.execute('insert into entries (task) values (?)', [request.form['new_task']])
    g.db.commit()
    flash('New task added to the list')
    return redirect(url_for('show_list'))


#@app.route('/<postID>', methods=['POST'])
#def remove_task():
#    g.db.execute('delete from entries WHERE id = ?', [postID])
#    g.db.commit()
#    flash('Selected tasks have been removed')
#    return redirect(url_for('show_list'))



if __name__ == '__main__':
    app.run()
