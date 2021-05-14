from connect_to_spotify import *
from query_artist import *

def breadth_first_search(artist, access, limit = 100):

    '''
        artist -> the input of the search algorithm.
        access -> the token to access Spotify data.
        limit -> the value by which to break the algorithm if met.
    '''

    songs = get_artist_songs(artist[1], access)
    stack = []
    dequeued = []
    adjacency_list = {}
    for artists in songs.values():
        for person in artists:
            name = person[0]
            if name != artist[0]:
                stack.append(person)
                source_target = (artist[0], name)
                if source_target not in adjacency_list.keys():
                    adjacency_list[(artist[0], name)] = 0
                adjacency_list[source_target] += 1

    while len(dequeued) != limit:
        head = stack[0]
        stack.pop(0)
        if head not in dequeued:
            songs = get_artist_songs(head[1], access)
            for artists in songs.values():
                for person in artists:
                    name = person[0]
                    if name != head[0]:
                        stack.append(person)
                        source_target = (head[0], name)
                        if source_target not in adjacency_list.keys():
                            adjacency_list[(head[0], name)] = 0
                        adjacency_list[source_target] += 1

                        if person not in stack and person not in dequeued:
                            stack.append(person)

            dequeued.append(head)

    return adjacency_list
