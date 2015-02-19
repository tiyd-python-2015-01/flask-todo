from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean


DATABASE = '/tmp/todo.db'
DEBUG = True
SECRET_KEY = 'this is hard'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False)
    completed_at = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)

    def __init__(self, text,due_date):
        self.todo = text
        self.due_date = due_date

    def __repr__(self):
        return "<Todo {}>".format(self.text)

@app.route('/')
def show_entries():
    current_todo_list = Todo.query.filter(Todo.completed_at==None).order_by(Todo.due_date.desc()).all()
    completed_todo_list = Todo.query.filter(Todo.completed_at!=None).order_by(Todo.completed_at.desc()).all()
    past_due_list = [elem for elem in current_todo_list if elem.due_date < datetime.utcnow()]
    return render_template('show_entries.html',
                            entries=current_todo_list,
                            completed=completed_todo_list,
                            pastdue = past_due_list)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    text =  request.form['todo']
    duedate = request.form['due_date']
    todo = Todo(text, datetime.strptime(duedate, '%Y-%m-%d'))
    db.session.add(todo)
    db.session.commit()
    flash('New to-do was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/delete', methods=['POST'])
def delete_entry():
    if not session.get('logged_in'):
        abort(401)
    ids = request.form.getlist('entry')
    for id in ids:
        todo = Todo.query.get(id)
        todo.completed_at = datetime.utcnow()
        db.session.add(todo)
    db.session.commit()
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
    manager.run()
