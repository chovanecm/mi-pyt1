import configparser
import time
import unittest

import click

from . import config
from . import twitter as tw
from . import twitter_web


@click.group()
def cli():
    pass


@cli.command()
@click.option("--keys", default="twitter_private.ini", help="Config file with api keys for accessinig the Twitter API")
def web(keys):
    twitter_web.app.config["TW_CONFIG_FILE"] = keys
    twitter_web.app.run(debug=True)



@cli.command()
@click.option("--keys", default="twitter_private.ini", help="Config file with api keys for accessing the Twitter API.")
@click.option("--tweet_count", default=3, help="Load this number of tweets")
@click.option("--refresh_time", default=30, help="Refresh time (seconds)")
@click.option("--lang", default=None, help="Tweets only in one specified language (cs, en, es...)")
@click.argument("search")
def console(keys, search, tweet_count, refresh_time, lang):
    session = tw.get_session(keys)
    tweets = tw.read_tweets_with_session(session, search, tweet_count, lang=lang)
    max_id = 0
    while True:
        tweets.reverse()
        for tweet in tweets:
            print(tweet["user"]["screen_name"] + " on " + tweet["created_at"])
            print(tweet["text"])
            max_id = max(int(tweet["id"]), max_id)
            print("")
        time.sleep(refresh_time)
        tweets = tw.read_tweets_with_session(session, search, since_id=max_id, lang=lang)
        print("Updated on %s" % str(time.localtime()))


def read_tweets(search, tweet_count=5, lang=None, session=None, api_key="", api_secret=""):
    """Public function reading tweets.
        Provide either a valid Twitter session or your Twitter api key and secret.

        Returns the tweets and a session you can reuse
        when calling the function the next time"""
    if (session is None):
        session = tw.twitter_session(api_key, api_secret)
    tweets = tw.read_tweets_with_session(session, search, tweet_count=tweet_count, lang=lang)
    return tweets, session


class MyTest(unittest.TestCase):
    def test(self):
        cfg = config.read_config("twitter.ini")
        self.assertEqual(cfg, ("YOUR KEY", "YOUR SECRET"))


@click.command()
def test():
    unittest.main()


def main():
    cli();
