import sqlite3
from flask import Flask, request, session, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


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
    text = db.Column(db.String(255))

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Todo {}>".format(self.text)

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', todos=todo_list)

@app.route('/add', methods=['POST'])
def add_todo():
    text = request.form['text_box']
    todo = Todo(text)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def complete():
    ids = request.form.getlist('entry')
    for id in ids:
        todo = Todo.query.get(id)
        db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    manager.run()
