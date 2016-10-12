from flask import Flask
from flask import url_for
from flask import render_template

import cv1
app = Flask(__name__)

@app.route("/")
def default():
    session = get_session("../")