from urllib import error, parse, request
import json

from connect_to_spotify import *

######################################################
# The purpose of this .py is to find an artist that  #
# is most similar to the original search.  The issue #
# with Spotify is that you cannot directly access a  #
# artist, so you need to work around that.  This is  #
# what we attempt to do here.                        #
######################################################

id = '7b2232f3e2364e5ebf1fd25a94abe6a3'
secret = '1ec94311bb0c4799a46bb24a15c82387'
token = get_access_token(id, secret)
def get_potential_artists(search, access):

    '''
        search -> the artist trying to be reached.
        access -> the access token for Spotify.
    '''

    # We need our header so that Spotify knows what we're doing.
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access)
    }

    # We need to format it according to how Spotify anticipates the query.
    search = search.strip().replace(' ', '+')

    # We form the actual query to pass into our request.
    qry = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(search)
    req = request.Request(qry, headers = headers)

    # We basically make sure that the search is valid.
    try:

        # If it is, we return the return in the form of a dict.
        resp = request.urlopen(req).read().decode('utf-8')

        return json.loads(resp)
    
    except error.HTTPError:

        # Otherwise, something went wrong.  This could be like
        # illegal characters (emojis) or something went wrong.
        print('Bad request!')
        
        return None

print(get_potential_artists('A$AP', token))

