from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, DateTimeField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from flaskr.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        t_user = User.query.filter_by(username=username.data).first()
        if t_user:
            raise ValidationError('That username is taken. Choose another one')


class LoginForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = URLField('Contest URL', validators=[DataRequired()])
    date = DateTimeField('Contest Date and Time', format='%Y-%m-%d %H:%M:%S')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
