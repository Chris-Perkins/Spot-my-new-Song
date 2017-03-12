# Slightly modified spotipy tutorial code. Just making sure this works. :)

import spotipy
import tkinter
from spotipy.oauth2 import SpotifyClientCredentials


# get the username of a user by extraction from URls
def extract_username(URl):
    if len(URl) > 13 and URl[:13] == "spotify:user:":
        return URl[13:]
    elif len(URl) > 30 and URl[:30] == "https://open.spotify.com/user/":
        return URl[30:]
    else:
        return URl


# get the user information using i/o
def get_user_information(sp):
    # get the user information
    user = None
    username = extract_username(input("Please enter your spotify URl\n"))
    while(user == None):
        try:
            return sp.user(username)
        except spotipy.SpotifyException:
            username = extract_username(input("Invalid username, please enter again\n"))


def main():
    sp = spotipy.Spotify()
    user = get_user_information(sp)


if __name__ == "__main__":
    main()