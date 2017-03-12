# Slightly modified spotipy tutorial code. Just making sure this works. :)
# pause on project until I'm able to get a callback URI

import spotipy
import tkinter


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
    #user = get_user_information(sp)
    #print(user)
    # testing with the different ways one could enter a spotify track.
    track = "spotify:track:5PwCuqzezD4a7mfxMNwk86"
    print(sp.track(track))
    track = sp.track("6ZtJwCyyH3HpRXpL1TI1Cp")
    print(track)
    l_tracks = list()
    l_tracks.append("6ZtJwCyyH3HpRXpL1TI1Cp")
    print(sp.recommendations(None, None, l_tracks, 2, None))


if __name__ == "__main__":
    main()