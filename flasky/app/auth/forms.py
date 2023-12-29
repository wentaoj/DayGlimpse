from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, \
    BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    upass = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        'Username (public, must have any combination of letters, numbers, or dots): ', 
        validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have any combination of letters, numbers, or dots.')
               ])
    dob = DateField('Date of Birth: ', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.today())
    uid = IntegerField(
        "UserID (integer only, unique Identifiers): ", 
        validators=[DataRequired()]
        )
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords re-entered must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class LogoutForm(FlaskForm):
    submit = SubmitField("Log Out")
