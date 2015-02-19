from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from .models import Todo
from .forms import TodoForm
from .forms import TodoDate
from . import app, db

@app.route('/')
def show_todos():
    current_todos = current_todos = Todo.query.filter(Todo.completed_at == None).order_by(Todo.expected_at).all()
    new_todo_form = TodoForm()
    new_todo_date = TodoDate()
    date_now = datetime.utcnow()
    return render_template("show_todos.html",
                           new_todo_form=new_todo_form,
                           new_todo_date=new_todo_date,
                           date_now=date_now,
                           todos=current_todos)


@app.route('/add', methods=['POST'])
def add_todo():
    form = TodoForm()
    date_form = TodoDate()
    if form.validate_on_submit():
        todo = Todo(form.text.data)
        todo.expected_at = date_form.completed_at.data
        db.session.add(todo)
        db.session.commit()
        flash("Your todo was created.")
    else:
        flash("Your todo could not be created.")
    return redirect(url_for('show_todos'))


@app.route('/finish', methods=['POST'])
def finish_todo():
    ids = request.form.getlist('todos')
    for id in ids:
        todo = Todo.query.get(id)
        todo.completed_at = datetime.utcnow()
        db.session.add(todo)
    db.session.commit()
    return redirect(url_for('show_todos'))


@app.route('/completed', methods=['POST'])
def show_completed():
    completed_todos = Todo.query.filter(Todo.completed_at != None).order_by(Todo.expected_at).all()
    return render_template("completed_todos.html",
                           finished=completed_todos)


@app.route('/return', methods=['POST'])
def return_to_main():
    return redirect(url_for('show_todos'))
