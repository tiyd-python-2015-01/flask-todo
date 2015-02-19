from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html",
                           todos=todo_list)


@app.route("/add", methods=['POST'])
def make_a_todo():
    text = request.form['text']
    todo = Todo(text)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/complete_tasks", methods=['POST'])
def complete_tasks():
    ids = request.form.getlist('todo')
    for id in ids:
        todo = Todo.query.get(id)
        db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    manager.run()
