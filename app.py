import math

from flask import Flask, render_template, g, request, redirect, url_for, session
from db import get_db
from account_app import account_app
import click
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "session_data"
Session(app, )
app.config['DATABASE'] = 'homepage.db'

app.register_blueprint(account_app)

@app.teardown_appcontext
def fuck_you(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def home():

    # cur.execute('select * from homepage')
    return render_template("home.html")

@app.route('/history')
def history():
    return render_template("history.html")



@app.route('/booklist')
def booklist():
    db = get_db(app)
    cur = db.cursor()

    genre_id = request.args.get("genre")
    page = int(request.args.get("page", 1))

    per_page = 25
    offset = per_page * (page - 1)

    all_genres = cur.execute("SELECT * FROM ganre").fetchall()

    if genre_id and genre_id != "all":
        books = (cur.execute("SELECT * FROM booklist "
                            "JOIN book_genre on booklist.id = book_genre.book_id "
                            "WHERE book_genre.genre_id = ? ORDER BY id DESC LIMIT ? OFFSET ?", (genre_id,per_page, offset,))
                 .fetchall())
        total_books = cur.execute("SELECT COUNT(*) FROM booklist JOIN book_genre on booklist.id = book_genre.book_id "
                                 "WHERE book_genre.genre_id = ?",(genre_id,)).fetchone()[0]
    else:
        books = cur.execute("SELECT * FROM booklist ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset,)).fetchall()
        total_books = cur.execute("SELECT COUNT(*) FROM booklist").fetchone()[0]
    print(books)



    # books = cur.execute("SELECT * FROM booklist ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset,)).fetchall()

    total_pages = math.floor((total_books + per_page - 1) / per_page)
    return render_template("book-list.html",
                           booklist=books,
                           page=page,
                           total_pages=total_pages,
                           all_genres=all_genres,
                           )

@app.route('/booklist/<int:book_id>')
def book_inside(book_id):
    db = get_db(app)
    cur = db.cursor()
    tag_id = request.args.get("tag")
    all_tags = cur.execute("SELECT * FROM tag "
                           "JOIN main.book_tag bt on tag.id = bt.tag_id "
                           "WHERE book_id = ?", (book_id,)).fetchall()
    book = cur.execute("SELECT * FROM booklist WHERE id = ?", (book_id,)).fetchone()
    return render_template("book-inside.html", book=book, all_tags=all_tags)

@app.route("/rate/<int:book_id>", methods=["POST"])
def rate(book_id):
    rating = int(request.form["rating"])
    user_id = session.get("user_id")
    db = get_db(app)
    cur = db.cursor()
    cur.execute("INSERT INTO ratings (book_id, user_id, rating) VALUES (?, ?, ?)", (book_id, user_id, rating))
    db.commit()
    return redirect(url_for("book_inside", book_id=book_id))


@app.route('/throne-of-glass')
def throne_of_glass():
    db = get_db(app)
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='throne' order by order_num").fetchall()
    return render_template('ThroneofGlass.html', books=books)

@app.route('/mistborn')
def mistborn():
    db = get_db(app)
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='mistborn' order by order_num").fetchall()
    return render_template('Mistborn.html', books=books)

@app.route('/potter')
def potter():
    db = get_db(app)
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='potter' order by order_num").fetchall()
    return render_template('Potter.html', books=books)

@app.route('/poppy')
def poppy():
    db = get_db(app)
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='poppy' order by order_num").fetchall()
    return render_template('PoppyWar.html', books=books)

@app.route('/gamethrone')
def gamethrone():
    db = get_db(app)
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='gamethrone' order by order_num").fetchall()
    return render_template('gamethrone.html', books=books)

@app.route('/stormlight')
def stormlight():
    db = get_db(app)
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='stormlight' order by order_num").fetchall()
    return render_template('stormlight.html', books=books)