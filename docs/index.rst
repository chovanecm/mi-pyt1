.. SimpleTwitter documentation master file, created by
sphinx-quickstart on Wed Nov  2 12:30:33 2016.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

Welcome to SimpleTwitter's documentation!
=========================================

Contents:

.. contents::
:local:

=========================================
What is SimpleTwitter
=========================================
SimpleTwitter is a console application, a web application and a library for searching for recent tweets.
It displays the most recent tweets matching your search query. In console mode, it refreshes periodically with new
tweets.

=========================================
Requirements and Installation
=========================================
SimpleTwitter requires some additional packages, namely Flask, requests and click. These should be installed
automatically together with the package. Before using the application, you need to configure it with your Twitter API
key and secret. See :ref:`api_keys` for more information.

Install the application using Test PyPi:

``pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi simpletwitter``

.. _api_keys:

=========================================
Obtaining Twitter API keys
=========================================
In order to use the application, providing your personal API key and API secret is necessary. This manual assumes you
have a valid Twitter account at disposal.

#. Navigate to `apps.twitter.com`_
#. Click "Create New App"
#. Fill in arbitrary name that nobody else uses (make something up), description and a URL (anything except of example.org) You don't have to fill the callback URL
#. Take your Consumer API key and Consumer Secret from the Keys and Token Access tab.
#. Place the keys in the following format to an ini file where no unauthorised person can access it. Keep in mind: your API key is like your password.

Example ``twitter_keys.ini``::

    [twitter]
    api_key = YOUR_KEY_HERE
    api_secret = YOUR_SECRET_HERE


=========================================
Running the Application
=========================================
------------------------
As a Console Application
------------------------
Run

``simpletwitter console --keys twitter_keys.ini konvalinka``

to get latest tweets from the world of flora (and fauna in the Prague area).
To restrict keys for certain language, use e.g.

``simpletwitter console --keys twitter_keys.ini --lang cs konvalinka``

The language code should follow the ISO standards.

You can also specify how many tweets to return or how often to check for new tweets (using ``--tweet_count`` and
``--refresh_time``, respectively). The refresh time takes integers (seconds) as an argument.

------------------------
As a Web Application
------------------------
Run

``simpletwitter web --keys twitter_keys.ini``

This will start the server bundled with Flask.
You should see something like

``* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit]``

Open the address and voilà, you are there.
The user interface is simple, but powerful (haha). This allows you to search for tweets quickly.

=========================================
API Documentation
=========================================
The following part documents the public API of the application:

.. automodule:: simpletwitter
:members:

=========================================
Examples
=========================================

.. testsetup:: *
import json
    with open("statuses.json") as file:
       responses = json.load(file)
    class simpletwitter():
        def read_tweets(self, search, tweet_count=5, lang=None, session=None, api_key="", api_secret=""):
            return responses
    simpletwitter = simpletwitter()

.. testcode::
len(simpletwitter.read_tweets("python", tweet_count=2, api_key="blabla", api_secret="huhuhu"))

.. testoutput::
2




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _apps.twitter.com: http://apps.twitter.com/