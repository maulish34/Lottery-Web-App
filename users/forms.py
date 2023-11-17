import re
from datetime import datetime

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField

from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo


def character_check(form, field):
    exclude_chars = "*?!'^+%&/()=}[]{$#@<>"
    print("character check")
    for char in field.data:
        if char in exclude_chars:
            raise ValidationError(f"Character {char} is not allowed.")
    print("character check")


def phone_check(form, field):
    p = re.compile(r"^\d{4}-\d{3}-\d{4}$")
    if not p.match(field.data):
        print("invalid phone")
        raise ValidationError("Phone number must be of the format: XXXX-XXX-XXXX")
    print("phone check")


def validate_password(form, field):
    p = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])")
    print(field.data)
    if not p.match(field.data):
        raise ValidationError(
            "Password must contain 1 digit, 1 lowercase letter and 1 uppercase letter."
        )
    print("pass check")


def validate_dates(form, field):
    p = re.compile(r"^([012][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)[0-9]{2}$")
    if not p.match(field.data):
        raise ValidationError("Date must be of the format: DD/MM/YYYY")


def validate_postcode(form, field):
    p = re.compile(
        r"^([A-Z][0-9]) ([0-9][A-Z]{2})|([A-Z][0-9]{2}) ([0-9][A-Z]{2})|([A-Z]{2}[0-9]) ([0-9][A-Z]{2})$"
    )
    if not p.match(field.data):
        raise ValidationError(
            "The postcode must be in one of the following formats: XY YXX or XYY YXX or XXY YXX,"
            " where X is any uppercase letter and Y is any digit"
        )


class RegisterForm(FlaskForm):
    email = StringField(
        validators=[DataRequired(message="Please fill in this field."), Email()]
    )
    firstname = StringField(
        validators=[
            DataRequired(message="Please fill in this field."),
            character_check,
        ]
    )
    lastname = StringField(
        validators=[
            DataRequired(message="Please fill in this field."),
            character_check,
        ]
    )
    birthdate = StringField(
        validators=[DataRequired(message="Please fill in this field."), validate_dates]
    )
    phone = StringField(
        validators=[
            DataRequired(message="Please fill in this field."),
            phone_check,
        ]
    )
    postcode = StringField(
        validators=[
            DataRequired(message="Please fill in this field."),
            validate_postcode,
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(message="Please fill in this field."),
            Length(min=6, max=12, message="Must be between 8 and 15 characters in length"),
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


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    pin = StringField(validators=[DataRequired()])
    postcode = StringField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()


class PasswordForm(FlaskForm):
    current_password = PasswordField(id="password", validators=[DataRequired()])
    show_password = BooleanField("Show password", id="check")
    new_password = PasswordField(
        validators=[
            DataRequired(),
            Length(
                min=6, max=12, message="Must be between 8 and 15 characters in length"
            ),
            validate_password,
        ]
    )
    confirm_new_password = PasswordField(
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Both new password fields must be equal"),
        ]
    )
    submit = SubmitField("Change Password")

