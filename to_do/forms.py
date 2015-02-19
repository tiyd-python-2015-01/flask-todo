from flask_wtf import Form
from wtforms import StringField, DateField
from wtforms.validators import DataRequired

class TodoForm(Form):
    text = StringField('text', validators=[DataRequired()])
    due_date = DateField('due_date')
