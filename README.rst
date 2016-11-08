SimpleTwitter
==========================
This is the simplest Twitter user interface you have ever seen.
You can run it via the command line or web interface.

We would like to remind you to read the LICENSE before doing anything with the work.

Do not forget to setup your Twitter keys on apps.twitter.com
and insert them into an INI file in the following format:
The default ini file is twitter_private.ini
[twitter]
api_key = YOUR KEY
api_secret = YOUR SECRET


To run the tests with your own API_KEY and API_SECRET, set these environment variables and delete
the content in tests/fixtures/betamax directory, but not the directory itself. Then run python setup.py test or pytest


Test pypi:
https://testpypi.python.org/pypi?%3Aaction=pkg_edit&name=simpletwitter

===========================
Building the documentation
===========================
First of all, install development requirements

``pip install -r docs-requirements.txt``

Then::
    cd docs
    make html
    make doctest
