# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/to_do.db'
DEBUG = True
SECRET_KEY = 'this is hard'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# initializes the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Connects to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Special functions to be used before and after requests.
# g is a special object that stores connection info

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Shows all entries in micronlog

@app.route('/')
def show_entries():
    cur = g.db.execute('select id, todo from entries order by id desc')
    entries = [(row[0],row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# Adds an etry to microblog if user is logged in

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (todo) values (?)', [request.form['todo']])
    g.db.commit()
    flash('New to-do was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/delete', methods=['POST'])
def delete_entry():
    if not session.get('logged_in'):
        abort(401)
    for checked in request.form.getlist('entry') :
        g.db.execute('delete from entries where id =?',checked)
    g.db.commit()
    flash('To-dos have been updated')
    return redirect(url_for('show_entries'))

# Login management
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

# Logout. using pop removes the user entry. No need to check if user loggedin
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# to start the application
if __name__ == '__main__':
    app.run()
