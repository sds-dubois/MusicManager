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

reset_history = False
search_liked_tracks = False
create_artist_network = False
show_best_subgraph = False
check_new_tracks = True
add_to_playlist = True
score_threshold = 10

username = os.environ.get("SPOTIPY_USERNAME")

def login(scope='user-library-read'):
    token = util.prompt_for_user_token(username, scope)    
    return(token)

def save_likes(liked_artists):
	output_file = open('liked_artists.csv', 'wb')
	pickle.dump(liked_artists,output_file)
	output_file.close()

def load_likes():
	input_file = open('liked_artists.csv', 'r')
	liked_artists = pickle.load(input_file)
	input_file.close()

	return liked_artists

def add_to_history(item,history):
	title = item['track']['name']
	id = 'spotify:artist:' + item['track']['artists'][0]['id']
	if not(id in history):
		history[id] = []
	history[id].append(title.lower())


def get_liked_tracks(p_name='Liked',history={}):
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
			liked_tracks.update([ item['track']['name'] for item in tracks['items'] ])
			liked_artists.update([ item['track']['artists'][0]['name'] for item in tracks['items'] ])
			map(lambda item: add_to_history(item, history=history),tracks['items'])

			while tracks['next']:
				print('go to next')
				liked_tracks.update([ item['track']['name'] for item in tracks['items'] ])
				liked_artists.update([ item['track']['artists'][0]['name'] for item in tracks['items'] ])
				map(lambda item: add_to_history(item, history=history),tracks['items'])
				tracks = sp.next(tracks)

			save_likes(liked_artists)

			output_file = open('history.csv', 'wb')
			pickle.dump(history,output_file)
			output_file.close()
			return history
		else:
			print('Error, cannot find playlist')

	else:
		print("Can't get token for", username)


if(reset_history):
	history = {}
else:
	input_file = open('history.csv', 'r')
	history = pickle.load(input_file)
	input_file.close()

if(search_liked_tracks):
	history = get_liked_tracks(history=history)
liked_artists = load_likes()

if(create_artist_network):
	generate_graph(en,liked_artists)

G = nx.read_yaml('artist_graph')
print('Loaded artist network : ' + str(len(G.nodes())) + ' nodes')

# scores = [d['score'] for n,d in G.nodes(data=True)]
best_nodes = [n for n in G.nodes() if G.node[n]['score'] > score_threshold]
print(str(len(best_nodes)) + ' selected artists')

if(show_best_subgraph):
	G_bests = G.subgraph(best_nodes)
	display_graph(G_bests)
	plt.show()

if(check_new_tracks):
	all_tracks,history = get_all_hot_songs(en,best_nodes,G,history)
	output_file = open('new_tracks.csv', 'wb')
	pickle.dump(all_tracks,output_file)
	output_file.close()
	output_file = open('history.csv', 'wb')
	pickle.dump(history,output_file)
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
