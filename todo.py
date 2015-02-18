import argparse
import json
import os
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import Flask, g, jsonify, render_template, request, abort


# Connection settings to connect to the RethinkDB server
RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
TODO_DB = 'todoapp'


# Setting up the app database
def dbSetup():
    '''The app will create a table 'todos' in the db specified by the
    'TODO_DB' variable. We'll creat the database and table here using
    ['db_create']'''
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(TODO_DB).run(connection)
        r.db(TODO_DB).table_create('todos').run(connection)
        print('Database setup completed. Now run the app without --setup.')
    except RqlRuntimeError:
        print('App database already exists. Run the app without --setup.')
    finally:
        connection.close()


app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    '''Use Flask's '@app.before_request' and '@app.teardown_request' for opening a
    db connection'''
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=TODO_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


@app.route("/todos", methods=['GET'])
def get_todos():
    '''Use 'r.table' to retrieve all existing tasks. It queries the db in
    response to a GET request from the browser. When 'table' isn't
    followed by an additional command it returns all documents in the table.'''
    selection = list(r.table('todos').run(g.rdb_conn))
    return json.dumps(selection)


@app.route("/todos", methods=['POST'])
def new_todo():
    '''Create a new TODO in repsonse to a POST request to '/todos' with a
    JSON paybload using 'table.insert'

    The 'insert' operation returns a single object specifying the number of
    successfully created objects and their corresponding IDs.'''

    inserted = r.table('todos').insert(request.json).run(g.rdb_conn)
    return jsonify(id=inserted['generated_keys'][0])


@app.route("/todos/<string:todo_id>", methods=['GET'])
def get_todo(todo_id):
    '''Retrieve a single todo. Every new task gets assigned a unique ID. The
    browser can retrieve a specific task by GET: '/todos/<todo_id>'. To query
    the db for a single document by its ID, we use the 'get' command.'''
    todo = r.table('todos').get(todo_id).run(g.rdb_conn)
    return json.dumps(todo)


@app.route("/todos/<string:todo_id>", methods=['PUT'])
def update_todo(todo_id):
    '''Update todo done as a 'PUT' request'. Save the update by 'replace' '''
    return jsonify(r.table('todos').get(todo_id).replace(request.json)
                    .run(g.rdb_conn))


@app.route("/todos/<string:todo_id>", methods=['PATCH'])
def patch_todo(todo_id):
    ''' PATCH request will merge JSON object stored in the db with the
     new one'''
    return jsonify(r.table('todos').get(todo_id).update(request.json)
                    .run(g.rdb_conn))


# Deleting a task
@app.route("/todos/<string:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    return jsonify(r.table('todos').get(todo_id).delete().run(g.rdb_conn))


@app.route("/")
def show_todos():
    return render_template('todo.html')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Flask todo app')
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        dbSetup()
    else:
        app.run(debug=True)
