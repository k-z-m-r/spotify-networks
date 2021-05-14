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

    # We want to make sure that this has the elements we need.
    # For example, if a dictionary is passed but it's not the right one.
    try:
        list_artists = potential_artists['artists']['items']
        list_artists = [(artist['name'], artist['id']) for artist in list_artists]

        # We check to see if it's an empty list, i.e. a bad query makes it through.
        # This should never happen, but just in case.
        if len(list_artists) == 0:
            print('Empty list!')
            return None

        # If there's only one result, then we just return the first.
        # There's no need to iterate, as we'll just return this entry.
        elif len(list_artists) == 1:
            return list_artists[0]

        else:

            # We remove whitespace.
            search = search.strip()

            # We define a way to measure the similarity of two strings using SequenceMatcher.
            similarity = lambda a, b: SequenceMatcher(None, a, b).ratio()

            # Here, we store the similarities.  We convert it to lower so that casing isn't an issue.
            similarities = [similarity(search.lower(), artist[0].lower()) for artist in list_artists]

            # Finding the max similarity is easy with numpy.
            max_similarity = argmax(similarities)
            top_match = list_artists[max_similarity]

            # A bit unnecessary, but it would be good to inform the user that the search
            # might not be right.  The cutoff is arbitrary, but 0.80 felt right.
            if similarities[max_similarity] < 0.80:
                print('We could not find an accurate result.  Did you enter the right artist?')
            
            # top_match is a tuple of (name, id)
            return top_match

    # Basically, it's not a dictionary in the structure that we want.
    except:
        print('Data in incorrect form!')
        return None

def get_artist_info(artist_id, access):

    '''
        artist_id -> the spotify uri of the desired artist.
        access -> the access token for Spotify.
    '''

    # We need our header so that Spotify knows what we're doing.
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access)
    }

    # We form the actual query to pass into our request.
    qry = 'https://api.spotify.com/v1/artists/{}'.format(artist_id)
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