from flask import Flask
from flask import url_for
from flask import render_template

import twitter_main
app = Flask(__name__)


@app.route("/")
@app.route("/<search>")
def default(search = "python"):
    session = twitter_main.get_session(app.config["TW_CONFIG_FILE"])
    tweets = twitter_main.read_tweets(session, search, tweet_count=None, since_id=None, lang=None)
    return render_template("twitter.html", tweets=tweets)

if __name__ == "__main__":
    app.run(debug=True)
