import json
import os

import betamax
import pytest
from betamax.cassette import cassette
from markupsafe import Markup

import simpletwitter.twitter as tw_api
import simpletwitter.twitter_web as tw

directory = os.path.dirname(os.path.realpath(__file__))


def sanitize_token(interaction, current_cassette):
    # Exit early if the request did not return 200 OK because that's the
    # only time we want to look for Authorization-Token headers
    if interaction.data['response']['status']['code'] != 200:
        return

    headers_list = [interaction.data['request']['headers'], interaction.data['response']['headers'],
                    interaction.data['response']['body']["string"]]

    for headers in headers_list:
        if (isinstance(headers, str)):
            headers = json.loads(headers)
        for header_to_remove in ["Authorization", "access_token"]:
            token = headers.get(header_to_remove)
            print("THIS IS %s " % type(token))
            # If there was no token header in the response, exit
            if token is None:
                continue

            if (not isinstance(token, list)):
                token = [token]
            for t in token:
                # Otherwise, create a new placeholder so that when cassette is saved,
                # Betamax will replace the token with our placeholder.
                current_cassette.placeholders.append(
                    cassette.Placeholder(placeholder='<AUTH_TOKEN>', replace=t)
                )


with betamax.Betamax.configure() as config:
    # tell Betamax where to find the cassettes
    # make sure to create the directory
    config.cassette_library_dir = '%s/fixtures/betamax' % directory
    config.before_record(callback=sanitize_token)


@pytest.fixture
def testapp():
    tw.app.config['TESTING'] = True
    return tw.app.test_client()


def read(file):
    with open("%s/fixtures/entities/%s.json" % (directory, file)) as f:
        return json.load(f)


@pytest.mark.parametrize('test_entity', ("hashtags", "media", "urls", "user_mentions"))
def test_entities(testapp, test_entity):
    json = read(test_entity)
    with tw.app.test_request_context("/"):
        out = tw.entities(json["text"], json["entities"])
    expected = Markup(json["test_expected_output"])
    assert out == expected


def test_format_entity():
    text = "Das Zugteam der SBB begrüsst Sie im ICN nach Bellinzona, Arth-Goldau, Zug, Zürich HB und wünscht Ihnen" \
           " eine angenehme Reise."
    prepend = "<endbahnhof>"
    append = "</endbahnhof>"
    replace_text = "Zürich Hauptbahnhof"
    entity = {"indices": [75, 84]}
    out = tw.format_entity(text, prepend, append, entity, replace_text)
    assert "Das Zugteam der SBB begrüsst Sie im ICN nach Bellinzona, Arth-Goldau, Zug," \
           " <endbahnhof>Zürich Hauptbahnhof</endbahnhof> und wünscht Ihnen" \
           " eine angenehme Reise." == out

    out = tw.format_entity(text, prepend, append, entity)
    assert "Das Zugteam der SBB begrüsst Sie im ICN nach Bellinzona, Arth-Goldau, Zug," \
           " <endbahnhof>Zürich HB</endbahnhof> und wünscht Ihnen" \
           " eine angenehme Reise." == out

    out = tw.format_entity(text, "", append, entity)
    assert "Das Zugteam der SBB begrüsst Sie im ICN nach Bellinzona, Arth-Goldau, Zug," \
           " Zürich HB</endbahnhof> und wünscht Ihnen" \
           " eine angenehme Reise." == out

    out = tw.format_entity(text, "<blabla>", "", entity)
    assert "Das Zugteam der SBB begrüsst Sie im ICN nach Bellinzona, Arth-Goldau, Zug," \
           " <blabla>Zürich HB und wünscht Ihnen" \
           " eine angenehme Reise." == out


def test_search_tweets(betamax_session):
    betamax_session.headers.update({'Accept-Encoding': 'identity'})
    tw_api.session_factory = lambda: betamax_session
    MAX_TWEETS = 5
    SEARCH_TEXT = "renfe"
    results, _ = tw_api.read_tweets(SEARCH_TEXT, tweet_count=MAX_TWEETS, lang="es",
                                    api_key=os.environ.get("API_KEY", None),
                                    api_secret=os.environ.get("API_SECRET", None))
    assert len(results) == MAX_TWEETS

    for tweet in results:
        assert tweet["lang"] == "es"
        assert SEARCH_TEXT in tweet["text"].lower()
