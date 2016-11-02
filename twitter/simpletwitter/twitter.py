import base64

import requests

from . import config


def session_factory():
    return requests.Session()

def twitter_session(api_key, api_secret):
    """Returns a Twitter Session"""
    session = session_factory()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
    }

    r = session.post('https://api.twitter.com/oauth2/token',
                     headers=headers,
                     data={'grant_type': 'client_credentials'})

    bearer_token = r.json()['access_token']

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req

    session.auth = bearer_auth
    return session


def read_tweets_with_session(session, search, tweet_count=None, since_id=None, lang=None):
    params = params = {"q": search}
    if since_id is not None:
        params["since_id"] = since_id
    if tweet_count is not None:
        params["count"] = tweet_count
    if lang is not None:
        params["lang"] = lang
    r = session.get("https://api.twitter.com/1.1/search/tweets.json", params=params)

    return r.json()["statuses"]


def get_session(key_file):
    api_key, api_secret = config.read_config(key_file)
    return twitter_session(api_key, api_secret)


def read_tweets(search, tweet_count=5, lang=None, session=None, api_key="", api_secret=""):
    """Public function reading tweets.
        Provide either a valid Twitter session or your Twitter api key and secret.

        Returns the tweets and a session you can reuse
        when calling the function the next time"""
    if (session is None):
        session = twitter_session(api_key, api_secret)
    tweets = read_tweets_with_session(session, search, tweet_count=tweet_count, lang=lang)
    return tweets, session
