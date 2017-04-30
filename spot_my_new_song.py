'''
TO DO:
-----
H = high priority
M = medium priority
L = low priority
-----
H: Playlist Selection
H: Album Selection
'''

import session_handling
import recommend_handling

# our main "page", where user will choose what they want to access
def table_of_commands(spotify_session):
    # default choice to start while loop
    choice = 0
    
    # remain on the table of contents page until we decide to quit
    while choice != 4:
        try:
            choice = int(input("How would you like to find your new songs?\n" +
                                "1 - Find new songs using a list of playlists\n" + 
                                "2 - Find new new using a list of albums\n" + 
                                "3 - Quit\n"))
            # if we want to use a playlist
            if choice == 1:
                recommend_handling.get_playlist_recommendations(spotify_session)
            # if we want to use a list of albums
            elif choice == 2:
                recommend_handling.get_album_recommendations(spotify_session)
            # if we want to quit
            elif choice == 3:
                quit_nicely()
            # invalid choice entered
            else:
                print("Invalid choice. Please enter a value between 1-4.\n")
        except ValueError:
            print("Value entered was not an integer. Please enter an integer value between 1-4.\n")


# quit the program nicely by stopping and waiting for input.
def quit_nicely():
    input("The program will now close. Please press enter to continue.")
    quit()


def main():
    print("Welcome to Spot my New Song!\n")
    print("You will now attempt to log on.\n")
    
    # get user credentials to log on
    spotify_session = session_handling.get_spotify_session()
    print("Logged on successfully!")
    # navigate to the table of contents
    table_of_commands(spotify_session)


if __name__ == "__main__":
    main()