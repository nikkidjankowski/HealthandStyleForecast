
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class UserAddForm(FlaskForm):
    """form for creating a user"""

    first_name = StringField("first_name", validators=[InputRequired(message="Name can't be blank")])
    last_name = StringField("last_name", validators=[InputRequired(message="Name can't be blank")])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LocationForm(FlaskForm):

    address = StringField('address', validators=[DataRequired()])

class HealthForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    haveit = BooleanField("Do you have this issue?")


#'btn-primary' if msg.id in likes else 