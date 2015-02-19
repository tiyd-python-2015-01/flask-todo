from datetime import datetime
from flask import render_template, request, flash, url_for, redirect, g
from .app import app, db, Todo
from .forms import TodoForm


@app.route('/')
def home_page():
    current_todos = Todo.query.filter(Todo.completed_at == None).all()
    completed_todos = Todo.query.filter(Todo.completed_at != None).all()
    return render_template('index.html', current_todos=current_todos,
                           completed_todos=completed_todos)


@app.route('/add_task', methods=['POST'])
def added_task():
    todo = Todo(request.form['to_do'])
    db.session.add(todo)
    db.session.commit()
    flash("You added: {}".format(request.form['to_do']))
    return redirect(url_for('home_page'))


@app.route('/complete_task', methods=['POST'])
def list_completion():
    for task_id in request.form.getlist('checkboxes'):
        todo = Todo.query.get(task_id)
        todo.completed_at = datetime.utcnow()
        db.session.add(todo)
    db.session.commit()
    return redirect(url_for('home_page'))
