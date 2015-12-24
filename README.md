# Music Manager 
**Personnalized music management tool directly on Spotify!** - *In development*

Uses [Echo Nest and Spotify API](http://static.echonest.com/enspex/) to analyze a user's music tastes and automatically create Spotify playlists with new songs to discover.  

### Setup
You should request a key for both Echo Nest and Spotify APIs. Then, you can define all the folowing environment variables: `SPOTIPY_CLIENT_ID`,`SPOTIPY_CLIENT_SECRET`,`SPOTIPY_REDIRECT_URI,SPOTIPY_USERNAME` (for Spotify) and `ECHO_NEST_API_KEY` (for Echo Nest). Once this is done, you'll be able to use this code.  
If you have any trouble, you can check [this](http://spotipy.readthedocs.org/en/latest/#authorized-requests).

### Getting Started
- On Spotify, create two playlists: an empty one named `ToDiscover` and one named `Liked` in which you may add several songs that you like.  
- Setup the song database, history, and artist network by running `main.py` with `reset_history=True`, `get_liked_tracks=True` and `create_artist_network=True` in the config file. This step may take a while.
- Get suggested songs by running `main.py` with `check_new_tracks=True` and `add_to_playlist=True` in the config file. These tracks will be added to the playlist `ToDiscover`.
- Listen these new songs! Like it ? run `$python player.py like track_id`. Not for you ?  run `$python player.py pass track_id`. You can easily get the `track_id` on Spotify with a right-click on the song, and choose `Copy spotify URI`.
- Want to add any other song not in your `ToDiscover` playlist ? just run `$python player.py save track_id` in the console.
- Want to get more recommended songs ? Just rebuilt the artist network and check for new tracks (config : `create_artist_network=True`, `check_new_tracks=True`, `add_to_playlist=True`).  


### Coming next
Analyzing your tastes with the song database built with music details and pass/like reactions !

### Dependencies
This projects uses [SpotiPy](https://github.com/plamere/spotipy) to access Spotify's API in python and [pyen](https://github.com/plamere/pyen) for Echo Nest.
It also uses [NetworkX](https://networkx.github.io/) for graphs.
