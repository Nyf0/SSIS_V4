from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators, StringField, SubmitField, SelectField, widgets
from wtforms.validators import ValidationError
import re

def validate_id_format(form, field):
    # Check if the ID matches the format YYYY-NNNN
    if not re.match(r'^\d{4}-\d{4}$', field.data):
        raise ValidationError('ID must be in the format YYYY-NNNN')

class studentForm(FlaskForm):
    id = StringField('ID', validators=[validators.DataRequired(), validate_id_format])
    pic = FileField('Profile', validators=[FileAllowed(['jpg', 'jpeg', 'png']), validators.DataRequired()])
    fname = StringField('First name', validators=[validators.DataRequired(message="This cannot be empty!"), validators.Length(min=3, max=255, message="First name must be at least 3 characters")])
    lname = StringField('Last name', validators=[validators.DataRequired(message="This cannot be empty!"), validators.Length(min=3, max=255, message="Last name must be at least 3 characters")])
    course = SelectField('Course', [validators.DataRequired(message="Must choose a course!")], choices=[], widget=widgets.ListWidget(prefix_label=False))
    gender = SelectField('Gender', [validators.DataRequired(message="This cannot be empty!")], choices=[('Male', 'Male'), ('Female', 'Female')],
                        option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    level = SelectField('Year level', [validators.DataRequired(message="This cannot be empty!")],
                       choices=[(1, 1), (2, 2), (3, 3), (4, 4)],
                       option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Add student')

class EditstudentForm(FlaskForm):
    id = StringField('ID', validators=[validators.DataRequired(), validate_id_format])
    pic = FileField('Profile', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    fname = StringField('First name', validators=[validators.DataRequired(), validators.Length(min=3, max=255, message="First name must be at least 3 characters")])
    lname = StringField('Last name', validators=[validators.DataRequired(), validators.Length(min=3, max=255, message="Last name must be at least 3 characters")])
    course = SelectField('Course', [validators.DataRequired(message="Must choose a course!")], choices=[], widget=widgets.ListWidget(prefix_label=False))
    gender = SelectField('Gender', [validators.DataRequired(message="This cannot be empty!")],
                         choices=[('Male', 'Male'), ('Female', 'Female')],
                         option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    level = SelectField('Year level', [validators.DataRequired(message="This cannot be empty!")],
                       choices=[(1, 1), (2, 2), (3, 3), (4, 4)],
                       option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Add student')
