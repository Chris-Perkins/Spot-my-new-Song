# Spot my new Song
Input your favorite albums and playlists, and, with the help of a simple algo-rhythm, find new songs! 

### How to Use:
  1. Open your terminal to the file path where Spot my New Song is located
  1. In the command line, run spot_my_new_song.py  
        *If an error occurs, please consult to the "To Get Started" section*
  1. Enter the URL you were redirected when prompted
  1. Follow on-screen instructions

### Requirements:
* [Python 3+](https://www.python.org/)
* [Spotipy](https://github.com/plamere/spotipy)  
* [A Spotify Access Token](https://developer.spotify.com/my-applications/#!/)  
<sub>*Set your callback URI to* ```http://localhost:8888/callback```<sub>

### To Get Started
Create a credentials.txt file where the spot my new song scripts are located, and input the following:  
  * Username = your_user_name  
  * Client-ID = your_client_id  
  * Secret Key = your_secret_key  
  *alternatively, you can simply run the spot my song script to generate this file.

**Disclaimer:** There is an error that occasionally occurs when fetching songs. This is not an error in this code, but rather an error in the Spotipy library.
