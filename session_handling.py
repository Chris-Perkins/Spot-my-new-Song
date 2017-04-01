'''
Back-end functions to help get the session
moved to separate file to avoid clutter in the future
'''

import spotipy
import spotipy.util as util
from spot_my_new_song import quit_nicely


# get client credentials
def get_spotify_session():
    # final variable detailing our scope/needed permissions
    scope = "playlist-read-private user-library-read"
    username, client_id, client_secret = get_credentials()
    try:
        # get access token
        token = util.prompt_for_user_token(username, scope, 
                                            client_id, client_secret,
                                            "http://localhost:8888/callback")
            
        # attempt to create a new spotify session
        spotify_session = spotipy.Spotify(auth = token)
        
        # raises the handled exception below if authentication was unsuccessful.
        spotify_session.me()
            
        # we have a valid session, so we return it.
        return spotify_session
    except spotipy.oauth2.SpotifyOauthError:
        print("Invalid credentials entered. Please edit your credentials then retry.")
        quit_nicely()
    except spotipy.client.SpotifyException:
        print("No credentials are set. Please edit your credentials in credentials.txt")
        quit_nicely()


# open the credentials file, return user, client id, and secret key from
# the file if we were successful in opening.
def get_credentials():
    try:
        file_credentials = open("credentials.txt", "r")
        client_username = extract_username(file_credentials.readline())
        client_id = file_credentials.readline()[12:]
        secret_key = file_credentials.readline()[13:]
        file_credentials.close()
        
        return (client_username.replace("\n", ""), 
                client_id.replace("\n", ""), 
                secret_key.replace("\n", ""))
    except IndexError:
        print("Invalid credentials entered. Please try again.")
        quit_nicely()
    except FileNotFoundError:
        print("Credentials file missing. Creating...")
        create_credentials_file()
        print("File created. Please edit the file to include your credentials.")
        quit_nicely()
        
        
# Create a credentials file
def create_credentials_file():
    file_credentials = open("credentials.txt", "w")
    file_credentials.write("Username = \n")
    file_credentials.write("Client-ID = \n")
    file_credentials.write("Secret Key = ")
    file_credentials.close()
    
    
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