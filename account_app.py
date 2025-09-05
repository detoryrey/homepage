from multiprocessing.resource_tracker import register

from flask import Blueprint, render_template
from db import get_db
account_app = Blueprint('account_app', __name__)

@account_app.route('/account')
def account():
    db = get_db(account_app)
    return 'Account';

@account_app.route("/register")
def register():
     return render_template("")

