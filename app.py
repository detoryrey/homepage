from flask import Flask, render_template
import sqlite3
app = Flask(__name__)


@app.route('/')
def home():

    # cur.execute('select * from homepage')
    return render_template("home.html")

@app.route('/throne-of-glass')
def throne_of_glass():
    db = sqlite3.connect('homepage.db')
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='throne' order by order_num").fetchall()
    return render_template('ThroneofGlass.html', books=books)

@app.route('/mistborn')
def mistborn():
    db = sqlite3.connect('homepage.db')
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='mistborn' order by order_num").fetchall()
    return render_template('Mistborn.html', books=books)

@app.route('/potter')
def potter():
    db = sqlite3.connect('homepage.db')
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='potter' order by order_num").fetchall()
    return render_template('Potter.html', books=books)


