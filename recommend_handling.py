'''
back-end functions to help get recommendations
created to help avoid clutter in spot_my_new_song
'''

import spotipy

SET_YES = {"yes", "y", "ya", "ye"}


# in: spotify session, a dictionary of songs
# out: a list of the corresponding song URIs
# to use with recommendations function
def get_list_song_URIs(spotify_session, dict_songs):
    list_URIs = list()
    
    for song in dict_songs["tracks"]["items"]:
        list_URIs.append(song["track"]["uri"])
    
    # while we have not visited every page, iterate through
    while dict_songs["tracks"]["next"]:
        # visit the next page...
        dict_songs["tracks"] = spotify_session.next(dict_songs["tracks"])
        
        # get all items in this page
        for item in dict_songs["tracks"]["items"]:
            list_URIs.append(item["track"]["uri"])
    
    return list_URIs

# in: spotify_session, list of song URIs
# out: list of recommendations
def get_recommendations(spotify_session, list_URIs):
    list_recommendations = list()
    
    # get recommendations based on every list of 5 songs (5 songs is max seed limit
    # per the Spotify API).
    for i in range(len(list_URIs) // 5 + (1 if len(list_URIs) % 5 != 0 else 0)):
        # get the recommendations for these 5 songs
        list_recommendations.extend(spotify_session.recommendations(seed_tracks = 
                                     list_URIs[i * 5 : min(i * 5 + 5, len(list_URIs))])["tracks"]
                                    )
    print("\n".join(str(x) for x in list_recommendations))

# get recommendations of playlists
def get_playlist_recommendations(spotify_session):
    
    # get the playlist we wish to access
    def get_playlist_choice():
        # skeleton function for future song selection
        def get_custom_song_selection(playlist):
            pass
        
        playlists = spotify_session.current_user_playlists()["items"]
        for i in range(len(playlists)):
            print("%d - %s" % (i + 1, playlists[i]["name"]))
        print("%d - Return to main menu" % (i + 2))
        
        choice = 0
        while choice != i + 2:
            try:
                choice = int(input(("\nPlease enter the index (%d - %d)" + 
                           " of the playlist you would like to select.\n") % (1, i + 2)))
                
                # playlist from list
                if choice > 0 and choice <= i + 1:
                    # arrays are 0 indexed. -1
                    correct_playlist = input("Use playlist \"%s\"? Y/N\n" 
                                             % playlists[choice - 1]["name"])

                    if correct_playlist.lower() in {"yes", "y", "ya", "ye"}:
                            return playlists[choice - 1]
                # custom playlist enter
                # return to main menu
                elif choice == i + 2:
                    print("\nReturning to main menu.\n")
                # not in range
                else:
                    print("Invalid index entered.\n" + 
                          "Please enter an integer value between %d and %d" % (1, i + 3))
            except ValueError:
                print("Non-integer value entered.\n" + 
                      "Please enter an integer value between %d and %d" % (1, i + 3))
    
    # entry point for this function
    def main():
        # list of songs/albums/artists we'll be getting recommendations from
        list_URIs = list()
        
        add_more = True
        while add_more:
            playlist = get_playlist_choice()
            
            results = spotify_session.user_playlist(spotify_session.me()["id"], playlist["id"],
                           fields="tracks,next")
            
            # get all song URIs from this playlist
            list_URIs.extend(get_list_song_URIs(spotify_session, results))
            
            print("%s successfully added.\n" % playlist["name"])
            
            add_more = input("Would you like to add another playlist? Y/N\n").lower() in SET_YES
        
            #print(spotify_session.recommendations(seed_artists = None, seed_albums = None, seed_tracks=list_songs, limit = 20))
            get_recommendations(spotify_session, list_URIs)
        
    main()


# skeleton of later function
def get_album_recommendations(spotify_session):
    list_URIs = list()
    
    add_more = True
    while add_more:
        try:
            album = spotify_session.album(input("Please enter an album URI\n"))
            print(album)
            
            #to-do: format multiple artists better
            artists = ""
            for artist in album["artists"]:
                artists = artists + artist["name"]
            
            if input("test").lower() in SET_YES:
                print("Got here")
            
            add_more = input("Would you like to add another playlist? Y/N\n").lower() in SET_YES
        except spotipy.client.SpotifyException:
            print("Invalid album id entered. Please enter a valid Album URI.")