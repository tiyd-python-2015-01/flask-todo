import sqlite3
from flask import Flask, request, session, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import datetime


DATABASE = '/tmp/todo.db'
DEBUG = True
SECRET_KEY = 'development-key'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    completed_at = db.Column(db.DateTime)
    complete_by = db.Column(db.DateTime)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Todo {}>".format(self.text)

@app.route('/')
def index():
    current_date = datetime.utcnow()
    current_todos = Todo.query.filter(Todo.completed_at == None).order_by(Todo.complete_by).all()
    completed_todos = Todo.query.filter(Todo.completed_at != None).all()
    return render_template('index.html',
                            current_date = current_date,
                            todos=current_todos,
                            completed=completed_todos[::-1])

@app.route("/add", methods=['POST'])
def add_todo():
    text = request.form['text_box']
    time = request.form['complete_by']
    todo = Todo(text)
    # converting HTML formatted date to python format
    if time != '':
        complete_by_date = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        todo.complete_by = complete_by_date
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/finish', methods=['POST'])
def complete():
    ids = request.form.getlist('entry')
    for id in ids:
        todo = Todo.query.get(id)
        todo.completed_at = datetime.utcnow()
        db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/completed')
def show_completed():
    completed_todos = Todo.query.filter(Todo.completed_at != None).all()
    return render_template('completed.html',
                            completed=completed_todos[::-1])

if __name__ == '__main__':
    manager.run()
