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
        print("%d - Enter a custom playlist" % (i + 2))
        print("%d - Return to main menu" % (i + 3))
        
        choice = 0
        while choice != i + 3:
            try:
                choice = int(input(("\nPlease enter the index (%d - %d)" + 
                           " of the playlist you would like to select.\n") % (1, i + 3)))
                
                # playlist from list
                if choice > 0 and choice <= i + 1:
                    # arrays are 0 indexed. -1
                    correct_playlist = input("Use playlist \"%s\"? y/n\n" 
                                             % playlists[choice - 1]["name"])

                    if correct_playlist.lower() in {"yes", "y", "ya", "ye"}:
                        return playlists[choice - 1]
                # custom playlist enter
                elif choice == i + 2:
                    playlist_url = input("Please enter a spotify URL for the playlist")
                # return to main menu
                elif choice == i + 3:
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
        playlist = get_playlist_choice()
        
    
    main()


# skeleton of later function
def get_album_recommendations(spotify_session):
    pass


# skeleton of later function
def get_song_recommendations():
    pass