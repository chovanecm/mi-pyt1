import requests
import base64
 
def twitter_session(api_key, api_secret):
    session = requests.Session()
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

