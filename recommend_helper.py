''' 
Recommendation helper to handle functions used in recommend_handling
'''

import spotipy

# Occurrence values to help weigh our suggestions
# False if it was not in library, true otherwise.
# Song in library valued very highly negative to prevent
# recommending a song that is already in one of these playlists.
DICT_OCCURRENCE_VALUES = {
                          "ARTIST": {False: 1, True: 4}, 
                          "ALBUM" : {False: 2, True: 5}, 
                          "SONG"  : {False: 3, True: int(-1e10)}
                         }

# Dictionary holding current weights of song recommendations
# Based off dictionary occurrence values.
DICT_OCCURRENCES = {}

# in: spotify session, a dictionary of songs
# out: a list of the corresponding song URIs
# to use with recommendations function
def get_list_songs(spotify_session, dict_songs):
    list_songs = list()
    
    for song in dict_songs["tracks"]["items"]:
        list_songs.append(song)
    
    # while we have not visited every page, iterate through
    while dict_songs["tracks"]["next"]:
        # visit the next page...
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])
        
        # get all items in this page
        for song in dict_songs["tracks"]["items"]:
            list_songs.append(song)
    
    return list_songs


# get recommendations from spotify for a list of songs.
def get_spotify_recommendations(spotify_session, dict_songs):
    list_recommendations = list()
    # list of 5 songs
    list_five_songs = list()
    
    i = 0
    # get recommendations based on every list of 5 songs (5 songs is max seed limit)
    # per the Spotify API).
    while dict_songs["tracks"]:
        for song in dict_songs["tracks"]["items"]:
            list_five_songs.append(song["track"]["uri"])
        
            # if we're on the 5th song or at the end of the list,
            # get recommendations for this list then clear list
            if (i % 5 == 0 and i != 0) or i + 1 == len(dict_songs):
                # get the recommendations for these 5 songs
                list_recommendations.extend(spotify_session.recommendations(
                    seed_tracks = list_five_songs)["tracks"])
            
                # reset our list
                list_five_songs = list()
        
            i += 1
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])
    
    return list_recommendations
    

# skeleton of later function
def get_recommendations(spotify_session, list_songs, limit):
    pass


# in: a song, whether or not the source of this song is the user
# out: none
# helper function for set_weights. Sets weights of songs received
def set_weights_helper(song, source_is_user):
    print(song)
    
    for artist in song["track"]["artists"]:
        if artist["uri"] not in DICT_OCCURRENCES:
            DICT_OCCURRENCES[artist["uri"]] = DICT_OCCURRENCE_VALUES["ARTIST"][source_is_user]
        else:
            DICT_OCCURRENCES[artist["uri"]] += DICT_OCCURRENCE_VALUES["ARTIST"][source_is_user]
    
    if song["track"]["album"]["uri"] not in DICT_OCCURRENCES:
        DICT_OCCURRENCES[song["track"]["album"]["uri"]] = DICT_OCCURRENCE_VALUES["ALBUM"][source_is_user]
    else:
        DICT_OCCURRENCES[song["track"]["album"]["uri"]] += DICT_OCCURRENCE_VALUES["ALBUM"][source_is_user]


# in: dict of songs, whether or the source is user's library
# out: none
# Used to help our recommending algorithm
# NOTE: Could be integrated with get_recommendations, but that
# makes functions confusing. No reason to do it other than
# overhead optimization by not iterating twice and not making copies of dicts.
def set_weights(spotify_session, dict_songs, source_is_user):
    # while we are on a page that exists...
    while dict_songs["tracks"]:
        # get all items in this page
        for song in dict_songs["tracks"]["items"]:
            set_weights_helper(song, source_is_user)
            
        # visit the next page...
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])