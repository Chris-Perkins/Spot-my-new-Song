'''
back-end functions to help get recommendations
created to help avoid clutter in spot_my_new_song
'''

import spotipy
import recommend_helper

# Values which indicate the user input yes
SET_YES = {"yes", "y", "ya", "ye"}


# get recommendations of playlists
def get_playlist_recommendations(spotify_session):
    # get the playlist we wish to access
    def get_playlist_choice():
        # get all playlists, then filter playlists where user is not owner.
        playlists = spotify_session.current_user_playlists()["items"]
        playlists = [playlist for playlist in playlists if playlist["owner"]["id"]
                     == spotify_session.me()["id"]]
        
        for i in range(len(playlists)):
            print("%d - %s" % (i + 1, playlists[i]["name"]))
        print("%d - Return to main menu" % (i + 2))
        
        choice = 0
        while choice != i + 2:
            try:
                choice = int(input(("\nPlease enter the index (%d - %d)" + 
                           " of the playlist you would like to select.\n> ") % (1, i + 2)))
                
                # playlist from list
                if choice > 0 and choice <= i + 1:
                    # arrays are 0 indexed. -1
                    correct_playlist = input("Use playlist \"%s\"? Y/N\n> " 
                                             % playlists[choice - 1]["name"])

                    if correct_playlist.lower() in SET_YES:
                        print()
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
                      "Please enter an integer value between %d and %d\n" % (1, i + 3))
    
    # entry point for this function
    def main():
        # list of songs/albums/artists we'll be getting recommendations from
        list_spotify_recommends = list()
        
        add_more = True
        while add_more:
            playlist = get_playlist_choice()
            
            # user defined go to main menu
            if playlist == None:
                return
            
            results = spotify_session.user_playlist(spotify_session.me()["id"], playlist["id"],
                                                    fields="tracks,next")
            
            # set recommend helper weights for this playlist
            recommend_helper.set_weights_user(spotify_session, results.copy())
            
            print("%s successfully added.\n" % playlist["name"])
            
            add_more = input("Would you like to add another playlist? Y/N\n> ").lower() in SET_YES
            print()
        
        # Include all recommended songs into Spotify's recommended results
        list_spotify_recommends.extend(recommend_helper.
                                       get_spotify_recommendations(spotify_session, 
                                                                   results.copy()))
        
        # set recommended song weights for songs in the list of recommendations
        recommend_helper.set_weights_recommended(spotify_session, 
                                                 list_spotify_recommends)
        
        # get Spot my New Song's recommendations based on weights inserted previously
        recommendations = recommend_helper.get_recommendations(spotify_session, 30)
        
        print("I recommend the following:")
        for song in recommendations:
            artist_string = ", ".join(x["name"] for x in song["artists"])
            print("%s: %s" % (artist_string, song["name"]))
        print()


        print("Would you like to create a playlist with these recommendations? Y/N")
        if (input("> ").lower() in SET_YES):
            print()
            create_playlist_with_songs(spotify_session, recommendations)
        else:
            print()
    
    # Where we first enter this function
    main()

# Creates a playlist with the given recommended songs
def create_playlist_with_songs(spotify_session, list_songs):
    playlist_name = None
    print("Name for the playlist? (Leave empty for default)")
    playlist_name = input("> ")
    print()

    print("Creating playlist...")

    # If we set a name, make it this name. Otherwise give default name
    playlist_name = playlist_name if (playlist_name != "") else "SMNS Discover"

    created_playlist = spotify_session.user_playlist_create(spotify_session.me()["id"],
                                                            playlist_name,
                                                            public=False)
    spotify_session.user_playlist_add_tracks(spotify_session.me()["id"],
                                             created_playlist["id"],
                                             list(song["id"] for song in list_songs),
                                             position=None)

    print("'%s' successfully created!\n" % playlist_name)
