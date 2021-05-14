from urllib import error, parse, request
from difflib import SequenceMatcher
from numpy import argmax
import json

from connect_to_spotify import *

######################################################
# The purpose of this .py is to find an artist that  #
# is most similar to the original search.  The issue #
# with Spotify is that you cannot directly access a  #
# artist, so you need to work around that.  This is  #
# what we attempt to do here.                        #
######################################################

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

def most_similar_artist(search, potential_artists):

    '''
        search -> the artist that the person is looking for.
        potential_artists -> a dict of
    '''
    try:
        list_artists = potential_artists['artists']['items']
        list_artists = [(artist['name'], artist['id']) for artist in list_artists]

        if len(list_artists) == 0:
            print('Empty list!')
            return None

        elif len(list_artists) == 1:
            return list_artists[0]

        else:
            search = search.strip()

            similarity = lambda a, b: SequenceMatcher(None, a, b).ratio()

            similarities = [similarity(search.lower(), artist[0].lower()) for artist in list_artists]
            max_similarity = argmax(similarities)
            
            top_match = list_artists[max_similarity]

            if similarities[max_similarity] < 0.80:
                print('We could not find an accurate result.  Did you enter the right artist?')
            
            return top_match

    except:
        print('Data in incorrect form!')
        return None
    