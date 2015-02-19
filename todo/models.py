from . import db

class Users(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.username)


class ToDo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(32), db.ForeignKey(Users.username))
    text = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    def __init__(self, owner, text):
        self.owner = owner
        self.text = text

    def __repr__(self):
        return "<Todo {}>".format(self.text)

class Notes(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(32), nullable=False)
    todo_reference = db.Column(db.Integer, db.ForeignKey(ToDo.id))
    text = db.Column(db.String(255), nullable=False)

    def __init__(owner, todo_reference, text):
        self.owner = owner
        self.todo_reference = todo_reference
        self.text = text

    def __repr__(self):
        return "<Notes {}>".format(self.text)
