'''
back-end functions to help get recommendations
created to help avoid clutter in spot_my_new_song
'''

import spotipy

SET_YES = {"yes", "y", "ya", "ye"}

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
        list_songs = list()
        
        add_more = True
        while add_more:
            playlist = get_playlist_choice()
            
            
            results = spotify_session.user_playlist(spotify_session.me()["id"], playlist["id"],
                           fields="tracks,next")
            tracks = results['tracks']
            
            for item in tracks['items']:
                list_songs.append(item['track']['uri'])
            
            while tracks['next']:
                tracks = spotify_session.next(tracks)
                for item in tracks['items']:
                    list_songs.append(item['track']['uri'])
            
            print("%s successfully added.\n" % playlist["name"])
            
            add_more = input("Would you like to add another playlist? Y/N\n").lower() in SET_YES
        
        print(list_songs)
        print(spotify_session.recommendations(seed_artists = None, seed_albums = None, seed_tracks=list_songs, limit = 20))
        return list_songs
    
    
    main()


# skeleton of later function
def get_album_recommendations(spotify_session):
    list_songs = list()
    
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