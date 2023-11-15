import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo


def character_check(form, field):
    exclude_chars = "*?!'^+%&/()=}[]{$#@<>"
    print('character check')
    for char in field.data:
        if char in exclude_chars:
            raise ValidationError(f"Character {char} is not allowed.")
    print('character check')


def phone_check(form, field):
    p = re.compile(r"^\d{4}-\d{3}-\d{4}$")
    if not p.match(field.data):
        print("invalid phone")
        raise ValidationError("Phone number must be of the format: XXXX-XXX-XXXX")
    print("phone check")


def validate_password(form, field):
    p = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])")
    print(field.data)
    if not p.match(field.data):
        raise ValidationError(
            "Password must contain 1 digit, 1 lowercase letter and 1 uppercase letter."
        )
    print("apss check")



class RegisterForm(FlaskForm):
    email = StringField(
        validators=[DataRequired(message="Please fill in this field."), Email()]
    )
    firstname = StringField(validators=[DataRequired(message="Please fill in this field."), character_check,])
    lastname = StringField(validators=[DataRequired(message="Please fill in this field."), character_check,])
    phone = StringField(validators=[DataRequired(message="Please fill in this field."), phone_check,])
    password = PasswordField(
        validators=[
            DataRequired(message="Please fill in this field."),
            Length(min=6, max=12),
            character_check,
            validate_password,
        ]
    )
    confirm_password = PasswordField(
        validators=[
            DataRequired(message="Please fill in this field."),
            EqualTo("password", message="Both password fields must be equal!"),
        ]
    )
    submit = SubmitField()
