'''
back-end functions to help get recommendations
created to help avoid clutter in spot_my_new_song
'''

import spotipy

# get recommendations of playlists
def get_playlist_recommendations(spotify_session):
    
    # get the playlist we wish to access
    def get_playlist_choice():
        playlists = spotify_session.current_user_playlists()
        print(playlists)
        for playlist in playlists:
            pass
    
    # entry point for this function
    def main():
        get_playlist_choice()
        
    
    main()


# skeleton of later function
def get_album_recommendations(spotify_session):
    pass


# skeleton of later function
def get_song_recommendations():
    pass