'''
back-end functions to help get recommendations
created to help avoid clutter in spot_my_new_song
'''

import spotipy

# get recommendations of playlists
def get_playlist_recommendations(spotify_session):
    
    # get the playlist we wish to access
    def get_playlist_choice():
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
            
    # skeleton function for future song slection
    def get_custom_song_selection(playlist):
        pass
    
    
    # entry point for this function
    def main():
        list_songs = list()
        add_more = True
        while add_more:
            playlist = get_playlist_choice()
            print("%s successfully added." % playlist["name"])
            
            if input("Would you like to use all songs in this playlist?\n" + 
                                 "Y to use all playlists, N to use a custom subset").lower() in {"yes", "y", "ya", "ye"}:
                #to-do: add all tracks here while staying under Spotify API limits
                pass
            else:
                # to-do: custom input tracks here
                print(playlist["tracks"])
            add_more = input("Would you like to add another playlist?").lower() in {"yes", "y", "ya", "ye"}
        
    
    
    main()


# skeleton of later function
def get_album_recommendations(spotify_session):
    pass


# skeleton of later function
def get_song_recommendations():
    pass