''' 
Recommendation helper to handle functions used in recommend_handling
'''

import spotipy

# Occurrence values to help weigh our suggestions
DICT_OCCURRENCE_VALUES = {"ARTIST": 1, "ALBUM": 2, "SONG":"3",
                        "ARTIST_LIBRARY": 4, "ALBUM_LIBRARY": 5}

# Dictionary holding current weights of song recommendations
# Based off dictionary occurrence values.
DICT_WEIGHTS = {}

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
def get_spotify_recommendations(spotify_session, list_songs):
    list_recommendations = list()
    
    # list of 5 songs
    list_5 = list()
    
    # get recommendations based on every list of 5 songs (5 songs is max seed limit)
    # per the Spotify API).
    for i in range(1, len(list_songs)):
        list_5.append(list_songs[i]["track"]["uri"])
        
        # if we're on the 5th song or at the end of the list,
        # get recommendations for this list then clear list
        if (i % 5 == 0 or i + 1 == len(list_songs)) and i != 0:
            # get the recommendations for these 5 songs
            list_recommendations.extend(spotify_session.recommendations(
                seed_tracks = list_5)["tracks"])
            
            list_5 = list()
            
    return list_recommendations
    

# skeleton of later function
def get_recommendations(spotify_session, list_songs, limit):
    pass


# in: dict of songs, whether or the source is user's library
# out: none
# Used to help our recommending algorithm
# NOTE: Could be integrated with get_recommendations, but that
# makes functions confusing. No reason to do it other than
# runtime optimization.
def set_weights(spotify_session, dict_songs, source_is_user):
    for song in dict_songs["tracks"]["items"]:
        print(song)
    
    # while we have not visited every page, iterate through
    while dict_songs["tracks"]["next"]:
        # visit the next page...
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])
        
        # get all items in this page
        for song in dict_songs["tracks"]["items"]:
            print(song)