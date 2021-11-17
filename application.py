from logging import error
import re
import sqlite3, hashlib, os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask.helpers import url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        db = conn.cursor()
        if 'email' not in session:
            isLogged = False
            firstName = ''
            numOfItems = 0
        else:
            isLogged = True
            db.execute("SELECT user_id, firstName FROM users WHERE email = ?", (session['email']))
            user_id, firstName = db.fetchall()
            # todo

    conn.close()
    return (isLogged, firstName, numOfItems)

@app.route('/')
def index():
    isLogged, firstName, numOfItems = getLoginDetails()
    # user_id = session['user_id']
    return render_template('index.html', isLogged = isLogged, firstName=firstName)

@app.route("/logInForm")
def signIn():
    if 'email' in session:
        return redirect(url_for*('/'))
    else:
        return render_template("login.html", error='404')


@app.route("/registerForm")
def registerForm():
    return render_template("register.html")

