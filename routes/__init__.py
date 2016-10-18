from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort

# from models.board import Board
from models.user import User

# 不加这一行会导致 mapper exception
#
# main = Blueprint('main', __name__)
#
#
# @main.route('/')
# def index_view():
#     return redirect(url_for('todo.index'))


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect(url_for('user.login_index'))
        return f(*args, **kwargs)
    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u.id != 1:
            abort(404)
        return f(*args, **kwargs)
    return function
