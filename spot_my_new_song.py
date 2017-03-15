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
            print("Invalid key info was entered. Please edit your credentials then retry.")
            quit_nicely()


# get the username information using i/o
def get_username():
    # get the user information
    username = extract_username(input("Please enter your spotify URl\n"))
    
    # create an un-authenticated session to check if our username is valid
    temp_session = spotipy.Spotify()
    
    # keep looping until a valid username is received.
    while True:
        try:
            # if this is not a valid username, we raise the handled exception.
            temp_session.user(username)
            
            # valid username, return it.
            return username
        except spotipy.SpotifyException:
            username = extract_username(input("Invalid username, please enter again\n"))


# our main "page", where user will choose what they want to access
def table_of_commands(spotify_session):
    # default choice to start while loop
    choice = -1
    
    # remain on the table of contents page until we decide to quit
    while choice != 4:
        choice = int(input("How would you like to find your new songs?\n" +
                           "1. Find new songs using a playlist\n" + 
                           "2. Find new songs using a list of songs\n" +
                           "3. Find new new using a list of albums\n" + 
                           "4. Quit\n"))
        # if we want to use a playlist
        if choice == 1:
            pass
        # if we want to use a list of songs
        elif choice == 2:
            pass
        # if we want to use a list of albums
        elif choice == 3:
            pass
        # if we want to quit
        elif choice == 4:
            quit_nicely()


# quit the program nicely by stopping and waiting for input.
def quit_nicely():
    input("The program will now close. Please press enter to continue.")
    quit()


def main():
    print("Welcome to Spot my New Song!\n")
    print("You will now attempt to log on.\n")
    
    # get user credentials to log on
    spotify_session = get_spotify_session()
    print("Logged on successfully!")
    
    # navigate to the table of contents
    table_of_commands(spotify_session)
    
    '''set_playlists = spotify_session.current_user_playlists()["items"]
    for index in range(len(set_playlists)):
        print("%d. %s - %s" % (index + 1, set_playlists[index]["name"], 
                               set_playlists[index]["owner"]["id"]))'''


if __name__ == "__main__":
    main()