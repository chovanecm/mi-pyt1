from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)


@app.route("/")
def hello():
    return 'MI-PYT je nejlepší předmět na FITu!'


@app.route("/hello/")
def hello_world():
    return url_for("profile", username="hroncok")


@app.route('/user/<username>')
def profile(username):
    return 'User {}'.format(username)


@app.route("/ciao/")
@app.route("/ciao/<user>")
def ciao(user=None):
    return render_template("hello.html", name=user)

if __name__ == '__main__':
    app.run(debug=True)