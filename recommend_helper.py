''' 
Recommendation helper to handle functions used in recommend_handling
'''

import spotipy
import random

# Occurrence values to help weigh our suggestions
# False if it was not in library, true otherwise.
# Song in library valued very highly negative to prevent
# recommending a song that is already in one of these playlists.
DICT_OCCURRENCE_VALUES = {
                          "ARTIST": {False: 1, True: 3}, 
                          "ALBUM" : {False: 2, True: 4}, 
                          "SONG"  : {False: 10, True: int(-1e10)}
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


# in: a valid spotify session, a dictionary of songs
# out: a list of Spotify's recommendations for songs
def get_spotify_recommendations(spotify_session, dict_songs):
    print("Fetching songs...")
    
    list_spotify_recommends = list()
    # list of 5 songs as referenced by https://developer.spotify.com/web-api/get-recommendations/
    list_five_songs = list()
    songCount = 0
    while dict_songs["tracks"]:
        for song in dict_songs["tracks"]["items"]:  
            songCount += 1
            
            if(songCount % 250 == 0):
                print("Parsing song #%d..." % songCount)
            
            list_five_songs.append(song["track"]["uri"])
        
            # if we're on the 5th song or at the end of the list,
            # get recommendations for this list then clear list
            if songCount % 5 == 0 or songCount + 1 == len(dict_songs["tracks"]["items"]):
                # get the recommendations for these 5 songs
                list_spotify_recommends.extend(spotify_session.recommendations(
                    seed_tracks = list_five_songs)["tracks"])
            
                # reset our list
                list_five_songs = list()        
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])
        
    print("Finished parsing %d songs!\n" % songCount)
    
    return list_spotify_recommends
    

# in: a valid spotify session, limit for amount of songs to return
# out: a list of "limit" length of recommendations for the user
def get_recommendations(spotify_session, limit):
    print("Fetching recommendations...")
    list_recommendations = list()
    recommendation_count = 0
    
    for song in LIST_RECOMMENDATION_SONGS:
        recommendation_count += 1
        # print every 1000th interval to notify the user that we're still processing
        if (recommendation_count % 1000 == 0):
            print("Parsing recommendation #%d" % recommendation_count)
        
        # set occurrence value based on values from set_weight(...)
        total_occurrence_value = 0
        total_occurrence_value += DICT_OCCURRENCES[song["album"]["uri"]]
        for artist in song["artists"]:
            total_occurrence_value += DICT_OCCURRENCES[artist["uri"]]
            
        # do not use URI here; some artists release songs as singles, then as parts of albums.
        # result is duplicate recommendations. Sorted to prevent different artist ordering from affecting.
        song["artists"].sort(key = lambda x : x["name"])
        artist_string = ", ".join(x["name"] for x in song["artists"])
        s = "%s: %s" % (artist_string, song["name"])
        total_occurrence_value += DICT_OCCURRENCES[s]
        
        # multiply by a random number to randomize our results
        # this allows the user to find multiple different lists of
        # recommendations without creating new playlists every time.
        total_occurrence_value = total_occurrence_value * random.random()
        
        # if this song is not already in our playlist
        if(total_occurrence_value > 0):
            list_recommendations.append([total_occurrence_value, song])
            
    print("Finished parsing %d recommendations!\n" % recommendation_count)
    
    # sort by the first value in recommendations (the weight of the song's recommendation)
    list_recommendations.sort(key = lambda x: x[0], reverse=True)
    
    list_output = list()
    # append as many songs as we can up to limit or the amount of songs
    for index in range(min(limit, len(list_recommendations))):
        # index 1 indicates the song (index 0 is the weight)
        list_output.append(list_recommendations[index][1])
    
    # reset everything for user later
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
        

# in: a valid spotify session, a list of spotify's recommended songs
# out: nothing
# sets the weights for all recommendations so we can parse do some
# math shenanigans later.
def set_weights_recommended(spotify_session, list_spotify_recommends):
    for song in list_spotify_recommends:
        # prevent the song from being added twice to list
        if song["uri"] not in SET_RECOMMENDATION_URIS:
            SET_RECOMMENDATION_URIS.add(song["uri"])
            LIST_RECOMMENDATION_SONGS.append(song)
        set_weights_helper(song, False)


# in: a song, bool indicating source is the user (true) or spotify (false)
# out: none
# helper function for set_weights. Sets weights of songs received in DICT_OCCURRENCES
def set_weights_helper(song, source_is_user):
    # Set weights for artists, albums, and the song URI itself.
    # artist weight
    for artist in song["artists"]:
        if artist["uri"] not in DICT_OCCURRENCES:
            DICT_OCCURRENCES[artist["uri"]] = 0
        DICT_OCCURRENCES[artist["uri"]] += DICT_OCCURRENCE_VALUES["ARTIST"][source_is_user]
    
    # album weight
    if song["album"]["uri"] not in DICT_OCCURRENCES:
        DICT_OCCURRENCES[song["album"]["uri"]] = 0
    DICT_OCCURRENCES[song["album"]["uri"]] += DICT_OCCURRENCE_VALUES["ALBUM"][source_is_user]
    
    # song weight
    # do not use song URI here; some artists release songs as singles, then as parts of albums.
    # result is duplicate recommendations. Sorted to prevent different artist ordering from affecting.
    song["artists"].sort(key = lambda x : x["name"])
    artist_string = ", ".join(x["name"] for x in song["artists"])
    s = "%s: %s" % (artist_string, song["name"])
        
    if s not in DICT_OCCURRENCES:
        DICT_OCCURRENCES[s] = 0
    DICT_OCCURRENCES[s] += DICT_OCCURRENCE_VALUES["SONG"][source_is_user]
