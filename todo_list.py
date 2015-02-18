import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
from contextlib import closing


#configuation
DATABASE = '/tmp/todo.db'
DEBUG = True
SECRET_KEY = 'i-am-a-secret-key'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('TODO_SETTINGS', silent=True)


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
def show_todos():
    cur = g.db.execute('select id,todo from entries order by id desc')
    entries = [dict(todo=row[1], id=row[0]) for row in cur.fetchall()]
    return render_template('show_todos.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_todo():
    g.db.execute('insert into entries (todo) values (?)',
                  [request.form['todo']])
    g.db.commit()
    flash('New todo was successfully posted')
    return redirect(url_for('show_todos'))


@app.route('/delete', methods=['POST'])
def delete_todo():
    g.db.execute('delete todo from entries where entries = ?'), [request.form['entry.id']]
    g.db.commit()
    return redirect(url_for('show_todos'))


if __name__ == '__main__':
    app.run(debug=True)
