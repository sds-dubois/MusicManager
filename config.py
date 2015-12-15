import pyen
import os

en = pyen.Pyen()

reset_history = False
create_db = False
search_liked_tracks = True
create_artist_network = True
show_best_subgraph = False
check_new_tracks = True
add_to_playlist = True
score_threshold = 10

username = os.environ.get("SPOTIPY_USERNAME")