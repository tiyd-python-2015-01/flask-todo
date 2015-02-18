import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE = '/tmp/todo.db'
DEBUG = True
SECRET_KEY = 'i-am-a-secret-key'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('TODO_SETTINGS', silent=True)
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Todo {}>".format(self.text)



@app.route('/')
def show_todos():
    todo_list = Todo.query.all()
    return render_template("show_todos.html",
                           todos=todo_list)


@app.route('/add', methods=['POST'])
def add_todo():
    text = request.form['text_box']
    todo = Todo(text)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('show_todos'))


@app.route('/delete', methods=['POST'])
def delete_todo():
    ids = request.form.getlist('todos')
    for id in ids:
        todo = Todo.query.get(id)
        db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('show_todos'))


if __name__ == '__main__':
    app.run(debug=True)
