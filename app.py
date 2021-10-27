import sqlite3
from flask import Flask, render_template, request
from flask_session import Session
from werkzeug.exceptions import abort, default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello people"