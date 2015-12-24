from artist_network import *
from song_db import *
from my_utils import *
from config import *

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import pickle

import pyen
import spotipy
import spotipy.util as util

if(reset_history):
	history = {}
else:
	input_file = open('history.csv', 'r')
	history = pickle.load(input_file)
	input_file.close()

if(search_liked_tracks):
	history = get_liked_tracks(history=history,reset_db=reset_db)
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
	get_new_suggestions(best_nodes,G,history)

if(add_to_playlist):
	token = login('playlist-modify-public')
	input_file = open('new_tracks.csv', 'r')
	new_tracks = pickle.load(input_file)
	input_file.close()
	if(token):
		add_new_tracks(new_tracks,username,token)
	else:
		print("Can't get token for", username)