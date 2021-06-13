from connect_to_spotify import *
from query_artist import *
import numpy as np

#########################################################
# The purpose of this .py is to genereate a BFS graph   #
# using an initial artist as the graph starting point.  #
# I also include functions to create the adjacency      #
# matrix so that the file isn't just one function.      #
#########################################################

def bfs(artist, access, limit = 100):

    '''
        artist -> the input of the search algorithm in form (name, id).
        access -> the token to access Spotify data.
        limit -> the value by which to break the algorithm if met.
    '''

    # Retrieve the songs for the starting artist.
    songs = get_artist_songs(artist[1], access)

    # Form the stack so that elements can be added to and removed from it.
    stack = []

    # Dequeued are the elements removed from the stack.
    dequeued = []

    # Adjacency list is the key-value pair of (source, target) -> weight.
    adjacency_list = {}

    # We iterate over the artists of the songs for each song. 
    # This is the initialization or the first layer of the BFS.
    for artists in songs.values():

        # We iterate over each person in the list of artists.
        for person in artists:

            # This is the actual Spotify name of the artist, not their uid.
            name = person[0]

            # We check to make sure that source, target isn't the same.
            if name != artist[0]:

                # We make sure that we haven't encountered this artist already
                # from the initial conditions.
                # If we haven't, then we add them to the stack and 
                # generate a tuple for the dictionary key.
                if name not in stack:
                    stack.append(person)

                source_target = (artist[0], name)

                # We check to make sure that they weren't already added in the adjacency list.
                # If not, we create an entry for them.
                if source_target not in adjacency_list.keys():
                    adjacency_list[(artist[0], name)] = 0

                # Then, we increment the weight by one.
                adjacency_list[source_target] += 1

            if len(adjacency_list) >= limit:
                break

        if len(adjacency_list) >= limit:
                break

    # Now, we actually start the breadth-first search.
    # We want to continue while the limit hasn't been reached
    # or the stack hasn't been fully emptied.
    while len(adjacency_list) < limit:
        if stack == []:
            break

        # We take the top of the stack and remove it from the stack.
        head = stack[0]
        stack.pop(0)

        # We check to make sure that we haven't already been to this artist.
        if head not in dequeued:

            # We effectively repeat what we did above, but now for any artist.
            songs = get_artist_songs(head[1], access)
            for artists in songs.values():
                for person in artists:
                    name = person[0]
                    if name != head[0]:

                        # Now, we include dequeued since this process actually dequeues artists.
                        if person not in stack or person not in dequeued:
                            stack.append(person)

                        source_target = (head[0], name)
                        if source_target not in adjacency_list.keys():
                            adjacency_list[(head[0], name)] = 0
                        adjacency_list[source_target] += 1

                    if len(adjacency_list) >= limit:
                        break

                if len(adjacency_list) >= limit:
                    break

            dequeued.append(head)

    return adjacency_list

def form_adjacency_matrix(adjacency_list, unweighted = True, undirected = True):

    '''
        adjacency_list -> a key-value pair in (edge -> weight) where the edge is a tuple (source, target).
        unweighted -> a Boolean flag on whether or not to allow the matrix to be unweighted.
        undirected -> a Boolean flag on whether or not to allow the matrix to be undirected.
    '''
    # We convert the keys into a numpy array for easier combination.
    numpy_adj = np.array(list(adjacency_list.keys()))
    source, target = numpy_adj.T

    # Get all of the unique artists for the nodes.
    nodes = np.union1d(np.unique(source), np.unique(target))
    N = nodes.shape[0]

    node_mapping = {node: idx for idx, node in enumerate(nodes)}

    # Create the empty array for the adjacency matrix.
    A = np.zeros((N, N))

    for edge in numpy_adj:
        node_1, node_2 = edge
        i, j = node_mapping[node_1], node_mapping[node_2]

        A[i, j] = adjacency_list[(node_1, node_2)]

    if undirected == True:
        B = np.triu(A) + np.tril(A).T
        A = B + B.T

    if unweighted == True:
        A = (A > 0).astype(int)

    return A