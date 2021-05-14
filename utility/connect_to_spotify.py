from urllib import error, parse, request
import json

######################################################
# The purpose of this .py is to form a connection to #
# the Spotify API such that we can retrieve a token. #
# This token is required to query any of their data. #
# In order to run this, urllib and json are needed.  #
# You will also need client credentials from         #
# the developer website.                             #
######################################################

def get_access_token(id, secret):

    '''
        id -> the client id from Spotify's API
        secret -> the client secret from Spotify's API
    '''

    # This is the location where you can query the token.
    url = 'https://accounts.spotify.com/api/token'

    # We need to pass it headers so that it knows what
    # information we're trying to retrieve.
    headers = {
                'grant_type': 'client_credentials',
                'client_id': id,
                'client_secret': secret,
                }

    # We make the query.  
    data = parse.urlencode(headers).encode()
    req =  request.Request(url, data = data)

    # This allows us to catch a bad request, i.e. bad user credentials.
    try:

        resp = request.urlopen(req).read().decode('utf-8')

        # If it succeeds, we convert the JSON to a Python dict.
        dict_resp = json.loads(resp)
        
        # Finally, we return the user token.
        return dict_resp['access_token']

    except error.HTTPError:

        # If we're here, then it failed and we should notify the person.
        print('Bad user credentials!')

        return None