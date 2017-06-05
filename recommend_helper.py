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
SET_RECOMMENDATION_URIS = set()
LIST_RECOMMENDATION_SONGS = list()

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
    list_spotify_recommends = list()
    # list of 5 songs
    list_five_songs = list()
    
    i = 1
    # get recommendations based on every list of 5 songs (5 songs is max seed limit)
    # per the Spotify API).
    while dict_songs["tracks"]:
        for song in dict_songs["tracks"]["items"]:
            list_five_songs.append(song["track"]["uri"])
        
            # if we're on the 5th song or at the end of the list,
            # get recommendations for this list then clear list
            if i % 5 == 0 or i + 1 == len(dict_songs["tracks"]["items"]):
                # get the recommendations for these 5 songs
                list_spotify_recommends.extend(spotify_session.recommendations(
                    seed_tracks = list_five_songs)["tracks"])
            
                # reset our list
                list_five_songs = list()
        
            i += 1
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])
    
    return list_spotify_recommends
    

# get recommendations based on occurrence values
def get_recommendations(spotify_session, limit):
    list_recommendations = list()
    for song in LIST_RECOMMENDATION_SONGS:
        # set occurrence value based on values from set_weight(...)
        total_occurrence_value = 0
        total_occurrence_value += DICT_OCCURRENCES[song["album"]["uri"]]
        for artist in song["artists"]:
            total_occurrence_value += DICT_OCCURRENCES[artist["uri"]]
        total_occurrence_value += DICT_OCCURRENCES[song["uri"]]
        
        # if this song is not already in our playlist
        if(total_occurrence_value > 0):
            list_recommendations.append([total_occurrence_value, song])
    
    list_recommendations.sort(key=lambda x: x[0], reverse=True)
    
    list_output = list()
    for index in range(min(limit, len(list_recommendations))):
        list_output.append(list_recommendations[index][1])
    
    # reset everything
    LIST_RECOMMENDATION_SONGS.clear()
    DICT_OCCURRENCES.clear()
    SET_RECOMMENDATION_URIS.clear()
    
    return list_output


# in: a valid spotify session, dict of songs
# out: none
# Used to help our recommending algorithm
# NOTE: Could be integrated with get_recommendations, but that
# makes functions confusing. No reason to do it other than
# overhead optimization by not iterating twice and not making copies of dicts.
def set_weights_user(spotify_session, dict_songs):
    # while we are on a page that exists...
    while dict_songs["tracks"]:
        # get all items in this page
        for song in dict_songs["tracks"]["items"]:
            set_weights_helper(song["track"], True)
            
        # visit the next page...
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])
        


def set_weights_recommended(spotify_session, list_spotify_recommends):
    for song in list_spotify_recommends:
        # prevent the song from being added twice to list
        if song["uri"] not in SET_RECOMMENDATION_URIS:
            SET_RECOMMENDATION_URIS.add(song["uri"])
            LIST_RECOMMENDATION_SONGS.append(song)
        set_weights_helper(song, False)


# in: a song, bool of if source of this song is the user
# out: none
# helper function for set_weights. Sets weights of songs received
def set_weights_helper(song, source_is_user):
    for artist in song["artists"]:
        if artist["uri"] not in DICT_OCCURRENCES:
            DICT_OCCURRENCES[artist["uri"]] = DICT_OCCURRENCE_VALUES["ARTIST"][source_is_user]
        else:
            DICT_OCCURRENCES[artist["uri"]] += DICT_OCCURRENCE_VALUES["ARTIST"][source_is_user]
    
    if song["album"]["uri"] not in DICT_OCCURRENCES:
        DICT_OCCURRENCES[song["album"]["uri"]] = DICT_OCCURRENCE_VALUES["ALBUM"][source_is_user]
    else:
        DICT_OCCURRENCES[song["album"]["uri"]] += DICT_OCCURRENCE_VALUES["ALBUM"][source_is_user]
    if song["uri"] not in DICT_OCCURRENCES:
        DICT_OCCURRENCES[song["uri"]] = DICT_OCCURRENCE_VALUES["SONG"][source_is_user]
    else:
        DICT_OCCURRENCES[song["uri"]] += DICT_OCCURRENCE_VALUES["SONG"][source_is_user]