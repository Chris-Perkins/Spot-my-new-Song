'''
TO DO:
-----
H = high priority
M = medium priority
L = low priority
-----
H: Playlist Selection
H: Song indices selection
M: Use files to enter in your client ID/secret ID rather than manual typing
L: put back-end functions in a different python file
'''

import spotipy
import spotipy.util as util
import tkinter
import os


# get the username of a user by extraction from URls
def extract_username(URl):
    # simply handling the different types of inputs for usernames
    # ways of inputting:
    # 1: spotify:user:username
    # 2: https://open.spotify.com/user/username
    # 3: username
    
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
    
    # create an un-authenticated session to check if our username is valid
    sp = spotipy.Spotify()
    
    # keep looping until a valid username is received.
    while True:
        try:
            # if this is not a valid username, we raise the handled exception.
            sp.user(username)
            
            # valid username, return it.
            return username
        except spotipy.SpotifyException:
            username = extract_username(input("Invalid username, please enter again\n"))


# get client credentials
def get_spotify_session():
    # final variable detailing our scope/needed permissions
    scope = "playlist-read-private user-library-read"
    
    # get the user we're trying to log in
    username = get_username()
    
    # loop until we receive a valid session
    while True:
        # get client id and secret keys
        client_id = input("Please enter your client ID key:\n")
        client_secret = input("Please enter your client secret key\n")
        
        try:
            # get access token
            token = util.prompt_for_user_token(username, scope, 
                                               client_id, client_secret,
                                               "http://localhost:8888/callback")
            
            # attempt to create a new spotify session
            sp = spotipy.Spotify(auth = token)
            
            # raises the handled exception below if authentication was unsuccessful.
            sp.me()
            
            # we have a valid session, so we return it.
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
    
    # print user info
    print(sp.me())
    
    set_playlists = sp.current_user_playlists()["items"]
    for index in range(len(set_playlists)):
        print("%d. %s - %s" % (index + 1, set_playlists[index]["name"], 
                               set_playlists[index]["owner"]["id"]))
    #print(sp.current_user_playlists()['items'][0]['name'])
    

if __name__ == "__main__":
    main()