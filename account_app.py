from dbm import sqlite3
from multiprocessing.resource_tracker import register

from werkzeug.security import generate_password_hash, check_password_hash

from acl_decorators.login_required import login_required
from flask import Blueprint, render_template, request, redirect, flash, url_for, session, jsonify
from db import get_db
import click
from datetime import datetime
account_app = Blueprint('account_app', __name__)


@account_app.route('/account')
def account():
    db = get_db(account_app)
    return 'Account';

@account_app.route('/profile')
def profile():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("account_app.log_in"))

    db = get_db(account_app)
    cur = db.cursor()
    user = cur.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

    if user is None:
        flash("User not found.")
        return redirect(url_for("account_app.log_in"))
    posts = cur.execute("SELECT * FROM post WHERE post.user_id = ? ORDER BY id DESC", (user_id,)).fetchall()

    cur.execute("""
                SELECT booklist.bookname, booklist.bookimg
                FROM user_books
                         JOIN booklist ON user_books.book_id = booklist.id
                WHERE user_books.user_id = ?
                  AND user_books.planned_book = 1
                """, (user_id,))
    planned_books = cur.fetchall()
    cur.execute("""
                SELECT booklist.bookname, booklist.bookimg
                FROM user_books
                         JOIN booklist ON user_books.book_id = booklist.id
                WHERE user_books.user_id = ?
                  AND user_books.read_book = 1
                """, (user_id,))
    read_books = cur.fetchall()

    return render_template("myprofile.html",
                           user=user,
                           posts=posts,
                           planned_books=planned_books,
                           read_books=read_books
                           )

def do_add_book(user_id, book_id, list_type):
    db = get_db(account_app)
    cur = db.cursor()

    cur.execute("SELECT planned_book, read_book FROM user_books WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    row = cur.fetchone()

    if row:
        if list_type == "read":
            cur.execute("""
            UPDATE user_books
            SET read_book = 1, planned_book = 0
            WHERE user_id = ? AND book_id = ?
        """, (user_id, book_id))
        elif list_type == "planned":
            cur.execute("""
            UPDATE user_books
            SET planned_book = 1, read_book = 0
            WHERE user_id = ? AND book_id = ?
        """, (user_id, book_id))
    else:
        planned = 1 if list_type == "planned" else 0
        read = 1 if list_type == "read" else 0
        cur.execute("INSERT INTO user_books(user_id, book_id, read_book, planned_book) VALUES (?, ?, ?, ?)", (user_id, book_id, read, planned))

    db.commit()

@account_app.route('/add_book', methods=['POST'])
def add_book():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    list_type = data.get('list_type')
    do_add_book(user_id, book_id, list_type)
    return jsonify({"success": True})

if __name__ == '__main__':
    account_app.run(debug=True)

def do_remove_book(user_id, book_id):
    db = get_db(account_app)
    cur = db.cursor()
    cur.execute("DELETE FROM user_books WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    db.commit()
@account_app.route('/remove_book', methods=['POST'])
def remove_book():
    data = request.json
    user_id = session.get("user_id")
    book_id = data.get('book_id')
    do_remove_book(user_id, book_id)
    return jsonify({"success": True})

@account_app.route('/add-post', methods=['POST'])
def add_post():
        content = request.form.get("content")
        user_id = session.get("user_id")

        if content:
            db = get_db(account_app)
            cur = db.cursor()
            cur.execute("INSERT INTO post (content, user_id) VALUES (?, ?)", (content, user_id))

            db.commit()
        return redirect(url_for("account_app.profile"))

if __name__ == "__main__":
    account_app.run(debug=True)


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

    return render_template("log_in.html") # user=session["user_id"]#)


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


