from flask import Flask, render_template, g
from db import get_db
from account_app import account_app
import click

app = Flask(__name__)

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

@app.route('/log-in')
def log_in():
    return render_template("log_in.html")

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
