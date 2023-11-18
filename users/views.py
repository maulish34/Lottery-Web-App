# IMPORTS
import logging
from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from markupsafe import Markup
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    login_manager,
)
from app import db, required_roles
from models import User
from users.forms import RegisterForm, LoginForm, PasswordForm

# CONFIG
users_blueprint = Blueprint("users", __name__, template_folder="templates")


# VIEWS
# view registration
@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash("Email address already exists")
            return render_template("users/register.html", form=form)

        role = "user"

        if not current_user.is_anonymous:
            if current_user.role == "admin":
                role = "admin"

        # create a new user with the form data
        new_user = User(
            email=form.email.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            birthdate=form.birthdate.data,
            phone=form.phone.data,
            postcode=form.postcode.data,
            password=form.password.data,
            total_logins="0",
            role=role,
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        if role != "admin":
            session["email"] = new_user.email
            logging.warning(
                "SECURITY - User registration [%s %s]",
                form.email.data,
                request.remote_addr,
            )

            # sends user to 2fa setup page
            return redirect(url_for("users.setup_2fa"))
        else:
            flash("New admin has been successfully added to the application.")
            return redirect(url_for("admin.admin"))
    # if request method is GET or form not valid re-render signup page
    return render_template("users/register.html", form=form)


# view user login
@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_anonymous:
        if not session.get("authentication_attempts"):
            session["authentication_attempts"] = 0
        print("attempts: " + str(session.get("authentication_attempts")))

        form = LoginForm()
        print("form displayed")
        if form.validate_on_submit():
            print("entered validate")
            user = User.query.filter_by(email=form.email.data).first()
            print(user.email)
            if (
                    not user
                    or not user.verify_password(form.password.data)
                    or not user.verify_pin(form.pin.data)
                    or not user.verify_postcode(form.postcode.data)
            ):
                logging.warning(
                    "SECURITY - Invalid log in [%s %s]",
                    form.email.data,
                    request.remote_addr,
                )
                session["authentication_attempts"] += 1
                if session.get("authentication_attempts") >= 3:
                    flash(
                        Markup(
                            "Number of incorrect login attempts exceeded. "
                            'Please click <a href="/reset">here</a> to reset.'
                        )
                    )
                    return render_template("users/login.html")
                attempts_remaining = 3 - session.get("authentication_attempts")
                print(attempts_remaining)
                flash(
                    "Please check your login details and try again, "
                    "{attempts} login attempts remaining".format(
                        attempts=attempts_remaining
                    )
                )
                return render_template("users/login.html", form=form)
            else:
                login_user(user)

                current_user.last_login = current_user.current_login
                current_user.last_ip = current_user.current_ip
                current_user.current_login = datetime.now()
                current_user.current_ip = request.remote_addr
                current_user.total_logins = str(int(current_user.total_logins) + 1)
                db.session.commit()
                logging.warning(
                    "SECURITY - Log in [%s %s %s %s]",
                    current_user.id,
                    current_user.email,
                    current_user.role,
                    request.remote_addr,
                )
                session["authentication_attempts"] = 0
                if current_user.role == "admin":
                    return redirect(url_for("admin.admin"))
                else:
                    return redirect(url_for("lottery.lottery"))

        return render_template("users/login.html", form=form)
    else:
        flash("You are already logged in.")
        return render_template("main/index.html")


# view user account
@users_blueprint.route("/account")
@login_required
def account():
    return render_template(
        "users/account.html",
        acc_no=current_user.id,
        email=current_user.email,
        firstname=current_user.firstname,
        lastname=current_user.lastname,
        phone=current_user.phone,
        birthdate=current_user.birthdate,
        postcode=current_user.postcode,
    )


@users_blueprint.route("/setup_2fa")
def setup_2fa():
    if "email" not in session:
        return redirect(url_for("403"))
    user = User.query.filter_by(email=session["email"]).first()
    if not user:
        del session["email"]
        return redirect(url_for("index"))

    return (
        render_template(
            "users/setup_2fa.html", username=user.email, uri=user.get_2fa_uri()
        ),
        200,
        {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@users_blueprint.route("/logout")
@login_required
def logout():
    session["authentication_attempts"] = 0
    logging.warning(
        "SECURITY - Log out [%s %s %s %s]",
        current_user.id,
        current_user.email,
        current_user.role,
        request.remote_addr,
    )
    logout_user()
    return redirect(url_for("index"))


@users_blueprint.route("/update_password", methods=["GET", "POST"])
@login_required
def update_password():
    form = PasswordForm()

    if form.validate_on_submit():
        if not current_user.password == form.current_password.data:
            flash("Incorrect current password. Please try again.")
            return redirect(url_for("users.update_password"))
        if current_user.password == form.new_password.data:
            flash(
                "The current password and new password can not be the same. Please try again."
            )
            return redirect(url_for("users.update_password"))
        else:
            current_user.password = form.new_password.data
            db.session.commit()
            flash("Password changed successfully")
            logging.warning(
                "SECURITY - Update password [%s %s %s %s]",
                current_user.id,
                current_user.email,
                current_user.role,
                request.remote_addr,
            )
            return redirect(url_for("users.account"))

    return render_template("users/update_password.html", form=form)
