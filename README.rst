SimpleTwitter
==========================
This is the simplest Twitter user interface you have ever seen.
You can run it via the command line or web interface.

We would like to remind you to read the LICENSE before doing anything with the work.

Please read the Documentation_ before getting started.


.. _Documentation: docs/_build/html/index.html

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

===========================
Running the tests
===========================

To run the tests with your own API_KEY and API_SECRET, set these environment variables and delete
the content in tests/fixtures/betamax directory, but not the directory itself. Then run python setup.py test or pytest

----------------------
On Linux/Unix
----------------------
::

    rm tests/fixtures/betamax/*
     API_KEY=YOUR_KEY API_SECRET=YOUR_SECRET python setup.py test
    
The extra space should prevent storing the command into your command history, so the keys wouldn't be saved.
Search for HISTCONTROL environment variable on the Internet if this doesn't work for you.

----------------------
On Windows
----------------------

::

    del tests/fixtures/betamax/*
    set API_KEY=YOUR_KEY
    set API_SECRET=YOUR_SECRET
    python setup.py test

