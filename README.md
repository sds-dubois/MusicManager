# Music Manager 
Personnalized music management tool directly on Spotify  - *In development*

Uses [Echo Nest and Spotify API](http://static.echonest.com/enspex/) to analyze a user's music tastes and automatically create Spotify playlists with new songs to discover.  

### Setup
You should request a key for both Echo Nest and Spotify APIs. Then, you can define all the folowing environment variables: `SPOTIPY_CLIENT_ID`,`SPOTIPY_CLIENT_SECRET`,`SPOTIPY_REDIRECT_URI,SPOTIPY_USERNAME` (for Spotify) and `ECHO_NEST_API_KEY` (for Echo Nest). Once this is done, you'll be able to use this code.  
If you have any trouble, you can check [this](http://spotipy.readthedocs.org/en/latest/#authorized-requests).

### Dependencies
This projects uses [SpotiPy](https://github.com/plamere/spotipy) to access Spotify's API in python and [pyen](https://github.com/plamere/pyen) for Echo Nest.
It also uses [NetworkX](https://networkx.github.io/) for graphs.
