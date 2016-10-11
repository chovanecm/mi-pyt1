import configparser
import time
import unittest

import click
import twitter as tw


@click.command()
@click.option("--keys", help="Config file with api keys for accessing the Twitter API.")
@click.option("--tweet_count", default=3, help="Load this number of tweets")
@click.option("--refresh_time", default=30, help="Refresh time (seconds)")
@click.option("--lang", default=None, help="Tweets only in one specified language (cs, en, es...)")
@click.argument("search")
def read_twitter_wall(keys, search, tweet_count, refresh_time, lang):
    api_key, api_secret = read_config(keys)
    session = tw.twitter_session(api_key, api_secret)
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


def read_config(keyfile):
    config = configparser.ConfigParser()
    config.read(keyfile)
    return config["twitter"]["api_key"], config["twitter"]["api_secret"]


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
    read_twitter_wall();