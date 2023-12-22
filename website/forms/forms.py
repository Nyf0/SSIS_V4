from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import validators, StringField, SubmitField, SelectField, widgets
from wtforms.validators import ValidationError
import re

def validate_id_format(form, field):
    # Check if the ID matches the format YYYY-NNNN
    if not re.match(r'^\d{4}-\d{4}$', field.data):
        raise ValidationError('ID must be in the format YYYY-NNNN')

def validate_file_size(form, field):
    # Check if the file size is less than or equal to 9MB
    max_size = 2 * 1024 * 1024  # 9MB in bytes
    if field.data and len(field.data.read()) > max_size:
        raise ValidationError('File size must be less than or equal to 2MB')
    
def validate_pic(form, field):
    if field.data:
        filename = field.data.filename
        if not (filename.lower().endswith(('.jpg', '.jpeg', '.png'))):
            raise ValidationError('Invalid file format. Please upload a JPEG or PNG image.')

class studentForm(FlaskForm):
    id = StringField('ID', validators=[validators.DataRequired(), validate_id_format])
    pic = FileField('Profile', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], message='Only JPEG or PNG images are allowed'),
        validate_file_size, validate_pic
    ])
    fname = StringField('First name', validators=[
        validators.DataRequired(message="This cannot be empty!"),
        validators.Length(min=3, max=255, message="First name must be at least 3 characters")
    ])
    lname = StringField('Last name', validators=[
        validators.DataRequired(message="This cannot be empty!"),
        validators.Length(min=3, max=255, message="Last name must be at least 3 characters")
    ])
    course = SelectField('Course', [validators.DataRequired(message="Must choose a course!")], choices=[], widget=widgets.ListWidget(prefix_label=False))
    gender = SelectField('Gender', [validators.DataRequired(message="This cannot be empty!")],
                        choices=[('Male', 'Male'), ('Female', 'Female')],
                        option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    level = SelectField('Year level', [validators.DataRequired(message="This cannot be empty!")],
                       choices=[(1, 1), (2, 2), (3, 3), (4, 4)],
                       option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Add student')

class EditstudentForm(FlaskForm):
    id = StringField('ID', validators=[validators.DataRequired(), validate_id_format])
    pic = FileField('Profile', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], message='Only JPEG or PNG images are allowed'),
        validate_file_size, validate_pic
    ])
    fname = StringField('First name', validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=255, message="First name must be at least 3 characters")
    ])
    lname = StringField('Last name', validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=255, message="Last name must be at least 3 characters")
    ])
    course = SelectField('Course', [validators.DataRequired(message="Must choose a course!")], choices=[], widget=widgets.ListWidget(prefix_label=False))
    gender = SelectField('Gender', [validators.DataRequired(message="This cannot be empty!")],
                         choices=[('Male', 'Male'), ('Female', 'Female')],
                         option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    level = SelectField('Year level', [validators.DataRequired(message="This cannot be empty!")],
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4)],
                        option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Add student')
