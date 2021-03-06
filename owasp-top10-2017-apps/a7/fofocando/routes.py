#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.log import error

from functools import wraps
import uuid
import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    make_response,
    session
)
from flask_bootstrap import Bootstrap
from model.password import Password
from model.db import DataBase

from flask_cors import CORS, cross_origin

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_pyfile('config.py')
database = DataBase(app.config['MYSQL_ENDPOINT'], app.config['MYSQL_USER'],
			app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])


def generate_csrf_token():
    '''
        Generate csrf token and store it in session
    '''
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid.uuid4())
    return session.get('_csrf_token')


app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.before_request
def csrf_protect():
    '''
        CSRF PROTECION
    '''
    if request.method == "POST":
        token_csrf = session.get('_csrf_token')
        form_token = request.form.get('_csrf_token')
        if not token_csrf or str(token_csrf) != str(form_token):
            error("csrf_protect",
                  "wrong value for csrf_token",
                  session.get("username"))
            return "ERROR: Wrong value for csrf_token"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('oops, session expired', "danger")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET'])
def root():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        psw = Password(str(request.form.get('password')))
        user_password, success = database.get_user_password(username)
        if not success or user_password == None or not psw.validate_password(str(user_password[0])):
            error("gossip", "User not found or wrong password", session.get('username'))
            flash("User not found or wrong password", "danger")
            return render_template('login.html')
        session['username'] = username
        return redirect('/gossip')
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        username = request.form.get('username')
        psw1 = request.form.get('password1')
        psw2 = request.form.get('password2')

        if psw1 == psw2:
            psw = Password(str(psw1))
            hashed_psw = psw.get_hashed_password()
            message, success = database.insert_user(str(username), hashed_psw)
            if success == 1:
                flash("New user added!", "primary")
                return redirect('/login')
            else:
                error("newuser", message, session.get('username'))
                return render_template('error.html')

        flash("Passwords must be the same!", "danger")
        return redirect('/register')
    else:
        return render_template('register.html')

@app.route('/gossip', methods=['GET'])
@login_required
def all_gossips():
    try:
        page = int(request.args.get('page'))
        if page < 1:
            raise TypeError
    except (TypeError, ValueError):
        page = 1

    search = request.args.get('search')
    offset = 10*(page - 1)
    search_flag = 0
    if search != None:
        gossips, success = database.search_gossips(offset, 10, search)
        search_flag = 1
    else:
        gossips, success = database.get_latest_gossips(offset, 10)
    if not success:
        error("all_gossips", gossips, session.get('username'))
        flash('Oops, something wrong happened!', "danger")
        return render_template('error.html')


    r = make_response(render_template('gossips.html', posts = gossips,search_text=search, search=search_flag))
    return r


@app.route('/gossip/<id>', methods=['GET', 'POST'])
@login_required
def gossip(id):
    if request.method == 'POST':
        comment = request.form.get('comment').encode('utf-8')
        user = session.get('username')
        date = datetime.datetime.now()
        message, success = database.post_comment(user, comment, id, date)
        if not success:
            error("gossip", message, session.get('username'))
            flash('Oops, something wrong happened', "danger")
            return render_template('error.html')
        flash('New comment added', "primary")
        return redirect('/gossip/{}'.format(id))
    else:
        gossip, success = database.get_gossip(id)
        if not success:
            error("gossip", gossip, session.get('username'))
            flash('Oops, something wrong happened!', "danger")
            return render_template('error.html')

        comments, success = database.get_comments(id)
        if not success:
            error("gossip", comments, session.get('username'))
            flash('Oops, something wrong happened!', "danger")
            return render_template('error.html')

        if comments == None:
            comments = []
        return render_template('gossip.html', post = gossip, comments = comments, id= id)

@app.route('/newgossip', methods=['GET', 'POST'])
@login_required
def newgossip():
    if request.method == 'POST':
        text = request.form.get('text', "").encode('utf-8')
        subtitle = request.form.get('subtitle', "").encode('utf-8')
        title = request.form.get('title', "").encode('utf-8')
        author = session.get('username', "")
        date = datetime.datetime.now()
        if author == '' or text == '' or subtitle == '' or title == '':
            error("gossip", "invalid parameters", session.get('username'))
            flash('Todos os campos devem ser preenchidos', "danger")
            return render_template('newgossip.html', title=title, subtitle=subtitle, text=text)
        database.post_gossip(author, text, title, subtitle, date)
        flash('New gossip added', "primary")
        return redirect('/gossip')

    else:
        return render_template('newgossip.html')


if __name__ == '__main__':
    app.run(port=8080, debug=False)
