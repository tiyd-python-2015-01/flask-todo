import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,\
    render_template, flash
from hashlib import md5
from contextlib import closing


DATABASE = '/tmp/to_do.db'
SECRET_KEY = 'development key'

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
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        cur = g.db.execute('select id, task from list where owner = ?',
                           [session.get('username')])
        entries = [item for item in cur.fetchall()]
        return render_template('show_entries.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not g.db.execute('select username from users where username = ?',
                            [request.form['username']]).fetchall():
            error = 'Invalid username'
        elif (md5(request.form['password'].encode('utf-8')).digest() !=
              g.db.execute(
              'select password from users where username = ?',
              [request.form['username']]).fetchall()[0][0]):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('Login successful!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Have a nice day!')
    return redirect(url_for('show_entries'))


@app.route('/create_user', methods=["GET", "POST"])
def create_user():
    error = None
    if request.method == 'POST':
        if not request.form['password'] or not request.form['username']:
            error = 'Username an password cannot be blank.'
        elif g.db.execute('select username from users where username = ?',
                          [request.form['username']]).fetchall():
            error = 'Username already in use.'
        else:
            g.db.execute(
                'insert into users (username, password) values (?, ?)',
                [request.form['username'],
                 md5(request.form['password'].encode('utf-8')).digest()])
            g.db.commit()
            flash('Account successfully created!')
            return redirect(url_for('login'))
    return render_template('create_user.html', error=error)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into list (owner, task) values (?, ?)',
                 [session.get('username'), request.form['todo']])
    g.db.commit()
    flash('New item added to list!')
    return redirect(url_for('show_entries'))


@app.route('/remove', methods=["POST"])
def remove_entry():
    for item in request.form.getlist('item'):
        owner, task = g.db.execute('select owner, task from list where id = ?',
                                   [item]).fetchall()[0]
        g.db.execute('delete from list where id = ?', [item])
        g.db.execute('insert into done (owner, task) values (?, ?)',
                     [owner, task])
        g.db.commit()
    flash('Item moved to completed list!')
    return redirect(url_for('show_entries'))


@app.route('/done', methods=["GET"])
def display_done():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        cur = g.db.execute('select task from done where owner = ?',
                           [session.get('username')])
        entries = [item for item in cur.fetchall()]
        return render_template('display_done.html', entries=entries)


if __name__ == '__main__':
    app.run()
