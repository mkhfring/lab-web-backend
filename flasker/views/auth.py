import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token

from ..models import User, db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        member = User.get_member(username)
        if member:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            User.add_member(username, generate_password_hash(password))

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if username is None or password is None:
            return jsonify({"msg": "No username of password is provided"}), 400

        error = None
        member = User.get_member(username)

        if member is None or \
                not check_password_hash(member.password, password):

            return jsonify({"msg": "Bad username or password"}), 401


        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        member = User.get_member_by_id(user_id)
        if member:
            g.user = member

        else:
            g.user = None


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
