from flask import Flask, render_template, request, redirect, url_for
from .models import Todo
from . import app, db

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
