from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


DATABASE = '/tmp/to_do.db'
DEBUG = True
SECRET_KEY = 'development-key'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    completed_at = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Todo {}>".format(self.text)


import to_do.views
