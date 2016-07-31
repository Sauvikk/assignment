from flask.ext.wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, validators, PasswordField, IntegerField, BooleanField
from .models import User
from  flask import flash
from wtforms.validators import NumberRange


class RegisterForm(Form):
    first_name = StringField("first_name",  [validators.Required("Please enter your first name.")])
    last_name = StringField("last_name",  [validators.Required("Please enter your last name.")])
    email = StringField("email",  [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email.")])
    password = PasswordField('password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("This email is already taken")
            return False
        else:
            return True


class LoginForm(Form):
    email = StringField("email",  [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email.")])
    password = PasswordField('password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return user
        else:
            flash("Invalid e-mail or password")
            return False


class FileUploadForm(Form):
    file = FileField("Choose a File", [validators.Required("Please enter a valid file.")])
    showFile = BooleanField('showFile', default=True)
    submit = SubmitField("Upload")


class FibonacciForm(Form):
    number = IntegerField("number", validators=[NumberRange(min=1, max=10)])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True
