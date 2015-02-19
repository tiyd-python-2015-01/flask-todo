from flask_wtf import Form
from wtforms import StringField
from wtforms import DateField
from wtforms.validators import DataRequired

class TodoForm(Form):
    text = StringField('text', validators=[DataRequired()])

class TodoDate(Form):
    completed_at = DateField('Goal date', format = '%m/%d/%Y',validators=[DataRequired()])
