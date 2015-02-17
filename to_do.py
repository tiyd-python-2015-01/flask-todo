from flask import Flask, render_template, request, flash, url_for, redirect, g
import sqlite3
from contextlib import closing


DATABASE = '/tmp/to_do.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def add_task(a_to_do):
    g.db.execute('insert into entries (task) values (?)',
                 [a_to_do])
    g.db.commit()
    return True


def get_tasks():
    cur = g.db.execute('select id, task from entries order by id desc')
    entries = [row for row in cur.fetchall()]
    return entries


def delete_task(task_id):
    g.db.execute('delete from entries where id=' + task_id)
    g.db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def added_task():
    new_to_do = request.form['to_do']
    add_task(new_to_do)
    flash('You successfully added: {}'.format(new_to_do))
    return redirect(url_for('home_page'))


@app.route('/list')
def list_page():
    return render_template('list.html', entries=get_tasks())


@app.route('/list', methods=['POST'])
def list_completion():
    [delete_task(task_id) for task_id in request.form.getlist('checkboxes')]
    return render_template('list.html', entries=get_tasks())


if __name__ == "__main__":
    app.run()
