from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


DATABASE = '/tmp/todo.db'
DEBUG = True
SECRET_KEY = 'development-key'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

from . import views
