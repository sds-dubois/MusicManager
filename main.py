from artist_network import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import pickle

import pyen
import spotipy
import spotipy.util as util

en = pyen.Pyen()

search_liked_tracks = False
create_artist_network = False
show_best_subgraph = False
check_new_tracks = False
add_to_playlist = True

username = os.environ.get("SPOTIPY_USERNAME")

def login(scope='user-library-read'):
    token = util.prompt_for_user_token(username, scope)    
    return(token)

def save_likes(liked_tracks,liked_artists):
	output_file1 = open('liked_tracks.csv', 'wb')
	pickle.dump(liked_tracks,output_file1)
	output_file1.close()

	output_file2 = open('liked_artists.csv', 'wb')
	pickle.dump(liked_artists,output_file2)
	output_file2.close()

def load_likes():
	input_file1 = open('liked_tracks.csv', 'r')
	liked_tracks = pickle.load(input_file1)
	input_file1.close()

	input_file2 = open('liked_artists.csv', 'r')
	liked_artists = pickle.load(input_file2)
	input_file2.close()

	return liked_tracks,liked_artists

def get_liked_tracks(p_name='Liked'):
	token = login()

	if token:
		sp = spotipy.Spotify(auth=token)
		playlists = sp.user_playlists(username)['items']
		playlist = None
		for p in playlists:
			if(p['name'] == p_name):
				playlist = p

		liked_tracks = set()
		liked_artists = set()
		if(playlist is not None):
			results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
			tracks = results['tracks']
			liked_tracks += [ item['track']['name'] for item in tracks['items'] ]
			liked_artists += [ item['track']['artists'][0]['name'] for item in tracks['items'] ]

			while tracks['next']:
				liked_tracks += [ item['track']['name'] for item in tracks['items'] ]
				liked_artists += [ item['track']['artists'][0]['name'] for item in tracks['items'] ]
				tracks = sp.next(tracks)

			save_likes(liked_tracks,liked_artists)

		else:
			print('Error, cannot find playlist')

	else:
		print("Can't get token for", username)


if(search_liked_tracks):
	get_liked_tracks()
liked_tracks,liked_artists = load_likes()

if(create_artist_network):
	generate_graph(en,liked_artists)

G = nx.read_yaml('artist_graph')
print('Loaded artist network : ' + str(len(G.nodes())) + ' nodes')

scores = [d['score'] for n,d in G.nodes(data=True)]
best_nodes = [n for n in G.nodes() if G.node[n]['score'] > score_threshold]
print(str(len(best_nodes)) + ' selected artists')

if(show_best_subgraph):
	G_bests = G.subgraph(best_nodes)
	display_graph(G_bests)
	plt.show()

if(check_new_tracks):
	all_tracks = get_all_hot_songs(en,best_nodes,liked_tracks)
	output_file = open('new_tracks.csv', 'wb')
	pickle.dump(all_tracks,output_file)
	output_file.close()

if(add_to_playlist):
	token = login('playlist-modify-public')
	input_file = open('new_tracks.csv', 'r')
	new_tracks = pickle.load(input_file)
	input_file.close()
	if(token):
		add_new_tracks(new_tracks,username,token)
	else:
		print("Can't get token for", username)	