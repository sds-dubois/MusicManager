import pyen
import os

en = pyen.Pyen()

reset_history = False
reset_db = False
search_liked_tracks = False
create_artist_network = False
show_best_subgraph = False
check_new_tracks = False
add_to_playlist = False

# artist network
score_threshold = 20
net_N_neighbors = 6
net_depth = 3

username = os.environ.get("SPOTIPY_USERNAME")