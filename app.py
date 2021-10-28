import sqlite3
import os
import requests
import re

from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, session, redirect, flash, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import abort, default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
 
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    # I had this as decorated() for about an hour and spent an hour debugging it ;-;
    return decorated

def createConnection():
    return sqlite3.connect("atlas.db")

@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = None
    con = createConnection()
    cur = con.cursor()
    posts = cur.execute("SELECT * FROM posts ORDER BY dateCreated DESC").fetchall()
    con.close()
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST":
        if (request.form.get("postTitle") == ""):
            return render_template("post.html", invalidTitle=True, invalidContent=False)
        if (request.form.get("postContent") == ""):
            return render_template("post.html", invalidTitle=False, invalidContent=True)
        con = createConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO posts (user_id, title, content, dateCreated) VALUES(?, ?, ?, ?)", (session["user_id"], request.form.get("postTitle"), request.form.get("postContent"), datetime.now()))
        con.commit()
        con.close()
        return redirect("/")
    return render_template("post.html", invalidTitle=False, invalidContent=False)

@app.route("/viewPost", methods=["GET", "POST"])
def viewPost():
    post_id = request.args.get("post_id")
    con = createConnection()
    cur = con.cursor()
    post = cur.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,)).fetchall()[0]
    con.close()
    return render_template("viewPost.html", post=post)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passwordRepeat = request.form.get("passwordRepeat")
        checkbox = request.form.get("checkbox")
        con = createConnection()
        cur = con.cursor()
        usernameMatches = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        con.close()
        if len(username) <= 4 or len(usernameMatches) > 0:
            return render_template("register.html", invalidUsername=True, invalidPassword=False, passwordMatch=False, invalidTerms=False)
        if len(re.findall("[a-zA-z]", password)) == 0 or len(re.findall("[0-9]", password)) == 0 or len(password) < 5:
            return render_template("register.html", invalidUsername=False, invalidPassword=True, passwordMatch=False, invalidTerms=False)
        if password != passwordRepeat:
            return render_template("register.html", invalidUsername=False, invalidPassword=False, passwordMatch=True, invalidTerms=False)
        if checkbox is None:
            return render_template("register.html", invalidUsername=False, invalidPassword=False, passwordMatch=False, invalidTerms=True)
        
        con = createConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, generate_password_hash(password)))
        con.commit()
        con.close()
        return redirect("/login")
        
    return render_template("register.html", invalidUsername=False, invalidPassword=False, passwordMatch=False, invalidTerms=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        con = createConnection()
        cur = con.cursor()
        usernameMatches = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        con.close()
        if not check_password_hash(usernameMatches[0][2], request.form.get("password")):
            return render_template("login.html", invalidPassword=True)
        session["user_id"] = usernameMatches[0][0]
        return redirect("/")
    return render_template("login.html", invalidPassword=False)

@app.route("/validateUsername")
def validateUsername():
    con = createConnection()
    cur = con.cursor()
    usernameMatches = cur.execute("SELECT * FROM users WHERE username = ?", (request.args.get("q"),)).fetchall()
    con.close()
    return jsonify(usernameMatches)

@app.route("/validatePassword")
def validatePassword():
    password = request.args.get("p")
    return jsonify({
        "letter" : len(re.findall("[a-zA-z]", password)) >= 1,
        "number" : len(re.findall("[0-9]", password)) >= 1,
        "length" : len(password) >= 5,
        "match" : password == request.args.get("rp")
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404