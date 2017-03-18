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
def extract_username(file_username):
    # simply handling the different types of inputs for usernames
    # ways of inputting:
    # 1: spotify:user:username
    # 2: https://open.spotify.com/user/username
    # 3: username
    username = file_username[11:]
    
    if len(username) > 13 and username[:13] == "spotify:user:":
        return username[13:]
    elif len(username) > 30 and username[:30] == "https://open.spotify.com/user/":
        return username[30:]
    else:
        return username


# get client credentials
def get_spotify_session():
    # final variable detailing our scope/needed permissions
    scope = "playlist-read-private user-library-read"
    username, client_id, client_secret = try_open_credentials_file()
    #username, client_id, client_secret = input().split()
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
        print("Invalid credentials entered. Please edit your credentials then retry.")
        quit_nicely()
    except spotipy.client.SpotifyException:
        print("No credentials are set. Please edit your credentials in credentials.txt")
        quit_nicely()


# determines whether a username is valid
def is_valid_username(username):
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


# open the credentials file, return user, client id, and secret key from
# the file if we were successful in opening.
def try_open_credentials_file():
    try:
        file_credentials = open("credentials.txt", "r")
        
        client_username = extract_username(file_credentials.readline())
        client_id = file_credentials.readline()[12:]
        secret_key = file_credentials.readline()[13:]
        
        file_credentials.close()
        
        return (client_username.replace("\n", ""), 
                client_id.replace("\n", ""), 
                secret_key.replace("\n", ""))
    except FileNotFoundError:
        print("Credentials file missing. Creating...")
        create_credentials_file()
        print("File created. Please edit the file to include your credentials.")
        quit_nicely()
    except IndexError:
        print("Invalid credentials entered. Please try again.")
        quit_nicely()


def create_credentials_file():
    file_credentials = open("credentials.txt", "w")
    file_credentials.write("Username = \n")
    file_credentials.write("Client-ID = \n")
    file_credentials.write("Secret Key = ")
    


def main():
    print("Welcome to Spot my New Song!\n")
    print("You will now attempt to log on.\n")
    
    # get user credentials to log on
    spotify_session = get_spotify_session()
    print("Logged on successfully!")
    
    # navigate to the table of contents
    table_of_commands(spotify_session)


if __name__ == "__main__":
    main()