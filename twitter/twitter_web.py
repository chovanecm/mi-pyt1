from flask import Flask
from flask import url_for

from flask import render_template
from flask import request
import sys

import twitter_main
from markupsafe import Markup

app = Flask(__name__)

DEFAULT_SEARCH_VALUE = "python"
@app.route("/")
def default():
    search = get_search_value()
    session = twitter_main.get_session(app.config["TW_CONFIG_FILE"])
    tweets = twitter_main.read_tweets(session, search, tweet_count=None, since_id=None, lang=None)
    return render_template("twitter.html", tweets=tweets, get_search_value=get_search_value)


def get_search_value():
    if "q" not in request.args:
        return DEFAULT_SEARCH_VALUE
    else:
        return request.args["q"]


@app.template_filter("entities")
def entities(text, entities):
    # We want to sort entities based on their position in the text
    # so we need to flatten all hasthags, media etc to one list
    flattened_entities = []

    def append_entity(name):
        if name in entities:
            flattened_entities.extend([{"type": name, "entity": entity} for entity in entities[name]])

    append_entity("hashtags")
    append_entity("media")
    append_entity("urls")
    append_entity("user_mentions")
    flattened_entities = sorted(flattened_entities, key=lambda entity: -entity["entity"]["indices"][0])

    for entity in flattened_entities:
        if entity["type"] == "user_mentions":
            text = format_entity(text, "<a href=\"http://twitter.com/" + entity["entity"]["screen_name"] + "\">",
                                 "</a>",
                                 entity["entity"])
        if entity["type"] in ["urls", "media"]:
            text = format_entity(text, "<a href=\"" + entity["entity"]["expanded_url"] + "\">", "</a>",
                                 entity["entity"],
                                 entity["entity"]["display_url"])
        if entity["type"] == "hashtags":
            text = format_entity(text, "<a href=\"" + url_for("default", q="#" + entity["entity"]["text"]) + "\">",
                                 "</a>",
                                 entity["entity"])
    return Markup(text)


def format_entity(text, prepend, append, entity, replace_text=None):
    if replace_text is None:
        # Insert the thing that was in the text
        format_to = (text[:entity["indices"][0]], prepend, text[entity["indices"][0]:entity["indices"][1]], append,
                     text[entity["indices"][1]:])
    else:
        # Insert something different instead of original entity text
        format_to = (text[:entity["indices"][0]], prepend, replace_text, append, text[entity["indices"][1]:])
    return ("%s%s%s%s%s") % format_to



if __name__ == "__main__":
    app.run(debug=True)
