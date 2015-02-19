from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, session
from hashlib import md5
from .models import Users, ToDo, Notes
from . import app, db


@app.route('/')
def main_menu():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/show_entries')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        current = ToDo.query.filter(
            ToDo.owner==session.get('username')).filter(
            ToDo.completed_at==None).all()
        for item in current:
            if item.due_date:
                item.due_date = item.due_date.strftime("%m/%d/%Y")
        return render_template('show_entries.html', entries=current)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = md5(request.form['password'].encode('utf-8')).digest()
        if not Users.query.get(username):
            error = 'Invalid username'
        elif not Users.query.get(username).password == password:
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
        elif Users.query.get(request.form['username']):
            error = 'Username already in use.'
        else:
            password = md5(request.form['password'].encode('utf-8')).digest()
            new_user = Users(request.form['username'], password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created!')
            return redirect(url_for('login'))
    return render_template('create_user.html', error=error)


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    elif request.method == 'POST':
        print(request.form['todo'])
        post = ToDo(session.get('username'), request.form['todo'])
        db.session.add(post)
        post.due_date = datetime.strptime(request.form['date'], "%m/%d/%y")
        db.session.commit()
        flash('New item added to list!')
        return redirect(url_for('show_entries'))
    else:
        return render_template('add_entry.html')


@app.route('/remove', methods=["POST"])
def remove_entry():
    if not session.get('logged_in'):
        abort(401)
    for item in request.form.getlist('item'):
        todo_update = ToDo.query.get(item)
        todo_update.completed_at = datetime.utcnow()
        db.session.add(todo_update)
    db.session.commit()
    flash('Item moved to completed list!')
    return redirect(url_for('show_entries'))


@app.route('/done', methods=["GET"])
def display_done():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        done = ToDo.query.filter(
            ToDo.owner==session.get('username')).filter(
            ToDo.completed_at!=None).all()
        for item in done:
            item.completed_at = item.completed_at.strftime("%m/%d/%Y")
        return render_template('display_done.html', entries=done)
