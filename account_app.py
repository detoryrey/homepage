from multiprocessing.resource_tracker import register

from werkzeug.security import generate_password_hash, check_password_hash

from acl_decorators.login_required import login_required
from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from db import get_db
import click
account_app = Blueprint('account_app', __name__)


@account_app.route('/account')
def account():
    db = get_db(account_app)
    return 'Account';

@account_app.route('/profile')
def profile():
    return render_template("myprofile.html")

@account_app.route('/log-in', endpoint='log_in', methods=('GET', 'POST'))
def log_in():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db(account_app)
        error = None
        username = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if username is None:
            error = "Incorrect username."
        elif not check_password_hash(username["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = username["id"]
            return redirect(url_for("account_app.profile"))

        flash(error)

    return render_template("log_in.html")


@account_app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        db = get_db(account_app)
        error = None

        if not username:
            error = "Username is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."


        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (email, username, password) VALUES (?, ?, ?)",
                    (email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError as e:
                print(e)
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("account_app.log_in"))

        flash(error, "error")


    return render_template("register.html")

@account_app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("logout"))


