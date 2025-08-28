from flask import Flask, render_template, g
import sqlite3
app = Flask(__name__)

app.config['DATABASE'] = 'homepage.db'

def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def home():

    # cur.execute('select * from homepage')
    return render_template("home.html")

@app.route('/throne-of-glass')
def throne_of_glass():
    db = get_db()
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='throne' order by order_num").fetchall()
    return render_template('ThroneofGlass.html', books=books)

@app.route('/mistborn')
def mistborn():
    db = get_db()
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='mistborn' order by order_num").fetchall()
    return render_template('Mistborn.html', books=books)

@app.route('/potter')
def potter():
    db = get_db()
    cur = db.cursor()
    books = cur.execute("SELECT * FROM books WHERE page='potter' order by order_num").fetchall()
    return render_template('Potter.html', books=books)


