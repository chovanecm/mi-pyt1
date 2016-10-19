import configparser
import time
import unittest

import click
import my_twitter as tw
import twitter_web


@click.group()
def cli():
    pass


@cli.command()
@click.option("--keys", help="Config file with api keys for accessinig the Twitter API")
def web(keys):
    twitter_web.app.config["TW_CONFIG_FILE"] = keys
    twitter_web.app.run(debug=True)


@cli.command()
@click.option("--keys", help="Config file with api keys for accessing the Twitter API.")
@click.option("--tweet_count", default=3, help="Load this number of tweets")
@click.option("--refresh_time", default=30, help="Refresh time (seconds)")
@click.option("--lang", default=None, help="Tweets only in one specified language (cs, en, es...)")
@click.argument("search")
def console(keys, search, tweet_count, refresh_time, lang):
    session = get_session(keys)
    tweets = read_tweets(session, search, tweet_count, lang=lang)
    max_id = 0
    while True:
        tweets.reverse()
        for tweet in tweets:
            print(tweet["user"]["screen_name"] + " on " + tweet["created_at"])
            print(tweet["text"])
            max_id = max(int(tweet["id"]), max_id)
            print("")
        time.sleep(refresh_time)
        tweets = read_tweets(session, search, since_id=max_id, lang=lang)
        print("Updated on %s" % str(time.localtime()))


def read_config(key_file):
    config = configparser.ConfigParser()
    config.read(key_file)
    return config.get("twitter", "api_key"), config.get("twitter","api_secret")


def get_session(key_file):
    api_key, api_secret = read_config(key_file)
    return tw.twitter_session(api_key, api_secret)


def read_tweets(session, search, tweet_count=None, since_id=None, lang=None):
    params = params = {"q": search}
    if since_id is not None:
        params["since_id"] = since_id
    if tweet_count is not None:
        params["count"] = tweet_count
    if lang is not None:
        params["lang"] = lang
    r = session.get("https://api.twitter.com/1.1/search/tweets.json", params=params)

    return r.json()["statuses"]


class MyTest(unittest.TestCase):
    def test(self):
        config = read_config("twitter.ini")
        self.assertEqual(config, ("YOUR KEY", "YOUR SECRET"))


@click.command()
def test():
    unittest.main()


if __name__ == "__main__":
    cli();
