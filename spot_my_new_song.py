# Slightly modified spotipy tutorial code. Just making sure this works. :)
# pause on project until I'm able to get a callback URI

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter
import os

scope = "playlist-read-private user-library-read"

# get the username of a user by extraction from URls
def extract_username(URl):
    if len(URl) > 13 and URl[:13] == "spotify:user:":
        return URl[13:]
    elif len(URl) > 30 and URl[:30] == "https://open.spotify.com/user/":
        return URl[30:]
    else:
        return URl


# get the username information using i/o
def get_username():
    # get the user information
    username = extract_username(input("Please enter your spotify URl\n"))
    sp = spotipy.Spotify()
    
    while True:
        try:
            # test if this is a valid username
            sp.user(username)
            return username
        except spotipy.SpotifyException:
            username = extract_username(input("Invalid username, please enter again\n"))


# get client credentials
def get_spotify_session():
    username = get_username()
    
    # if we have a cached token, we don't need client ID/secret keys.
    if os.path.isfile(".cache-" + username):
        token = util.prompt_for_user_token(username, "user-library-read",
                                           "x", "x", "x")
        return spotipy.Spotify(auth = token)
    
    while True:
        client_id = input("Please enter your client ID key:\n")
        client_secret = input("Please enter your client secret key\n")
        
        try:
            token = util.prompt_for_user_token(username, scope, 
                                               client_id, client_secret,
                                               "http://localhost:8888/callback")
            sp = spotipy.Spotify(auth = token)
            
            # run this command to check if we logged in successfully.
            sp.me()
            
            return sp
        except spotipy.oauth2.SpotifyOauthError:
            print("Invalid key info was entered. Please try again.")


def main():
    # testing with the different ways one could enter a spotify track.
    sp = get_spotify_session()
    track = "spotify:track:5PwCuqzezD4a7mfxMNwk86"
    print(sp.track(track))
    track = sp.track("6ZtJwCyyH3HpRXpL1TI1Cp")
    print(track)
    l_tracks = list()
    l_tracks.append("6ZtJwCyyH3HpRXpL1TI1Cp")
    print(sp.recommendations(None, None, l_tracks, 2, None))
    
    # print user info
    print(sp.me())
    print(sp.current_user_playlists())
    

if __name__ == "__main__":
    main()