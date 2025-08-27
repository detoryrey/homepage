from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
# db = sqlite3.connect('homepage.db')
# cur = db.cursor()

@app.route('/')
def home():

    # cur.execute('select * from homepage')
    return render_template("home.html")

@app.route('/throne-of-glass')
def throne_of_glass():
    return render_template('ThroneofGlass.html')



