import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import pickle

import pyen
import spotipy
import spotipy.util as util

N_neighbors = 6
depth = 3
ratio_score_songs = 4
# N_songs_per_artist = 3

def get_id(response):
	if(len(response) > 0):
		return True,response[0]
	else:
		print("No result", response)
		return False,""

def search_similar_artists(en,artist_list,N_neighbors=3,depth=3,pop_threshold=0.45):
	G = nx.DiGraph()
	temp = [(en.get('artist/search', name=a, bucket=['hotttnesss','id:spotify'], results=1)['artists']) for a in artist_list]
	queue = []
	for t in temp:
		b,artist = get_id(t)
		if(b):
			queue.append(artist)
			G.add_node(artist['id'],name=artist['name'], hotness = artist['hotttnesss'],depth=0,score=8,
						spotify_id=artist['foreign_ids'][0]['foreign_id'])
	done = set()
	# print(queue)
	queue2 = []

	for d in xrange(depth):
		print('Level '+str(d))
		while len(queue) > 0:
		    artist = queue.pop(0)
		    if artist['id'] not in done:
		        response = en.get('artist/similar', id=artist['id'], bucket=['hotttnesss','id:spotify'])['artists']
		        done.add(artist['id'])

		        r = 0
		        for a in response[:N_neighbors]:
					r += 1
					if not (a['id'] in done or a['id'] in queue or a['id'] in queue2 or a['hotttnesss'] < pop_threshold):
						if('foreign_ids' in a):
							G.add_node(a['id'],name=a['name'], hotness = a['hotttnesss'],depth=(d+1),score=0,
									spotify_id=a['foreign_ids'][0]['foreign_id'])
							# print a['id'], a['name']
							queue2.append(a)
					if (a['hotttnesss'] >= pop_threshold and 'foreign_ids' in a):
						G.add_edge(artist['id'],a['id'],rank=r)
					else:
						print 'Removed',a['id'], a['name']

		queue = list(queue2)
		queue2 = []

	return G

def generate_graph(en,liked_artists):
	G = search_similar_artists(en,liked_artists,N_neighbors=N_neighbors,depth=depth)
	# adding nodes' score
	for n in G.nodes():
		d = G.degree(n)
		G.node[n]['score'] += scoring(d,G.node[n]['hotness'],G.node[n]['depth'])
	nx.write_yaml(G,'artist_graph')

def scoring(degree,popularity,depth):
	# degree is between 0 and N_neighbors=6
	# popularity is between 0<pop_threshold and 1
	# depth is between 0 and depth=3
	return( degree + 5.*popularity - 1.5*depth)

def display_graph(G):
	col = ['red','blue','green','orange']
	sizes =dict((n,d['hotness']) for n,d in G.nodes(data=True))
	names =dict((n,d['name']) for n,d in G.nodes(data=True))
	colors =dict((n,col[d['depth']]) for n,d in G.nodes(data=True))
	widths = [0.3*(N_neighbors-d['rank'])+0.5 for n1,n2,d in G.edges(data=True)]

	plt.figure(figsize=(30,25))
	graph_pos = nx.spring_layout(G)
	center = np.mean(graph_pos.values())
	for n in graph_pos.keys():
		graph_pos[n] = center + (graph_pos[n]-center)/(0.2*(depth-G.node[n]['depth'])+1.)
	nx.draw_networkx_nodes(G, graph_pos, nodelist=graph_pos.keys(), node_size=[30.*(1+sizes[n])**6 for n in graph_pos.keys()],
							node_color=[colors[n] for n in graph_pos.keys()], alpha=0.5)
	nx.draw_networkx_edges(G, pos=graph_pos, width=widths)
	nx.draw_networkx_labels(G, graph_pos,labels = dict((n,names[n]) for n in graph_pos.keys()), font_size=12, font_family='sans-serif')

def connected_components(G):
	comps = sorted(list(nx.strongly_connected_component_subgraphs(G,copy=True)),key=len,reverse=True)
	for i in xrange(3):
		G2 = comps[i]
		print(i,'th component nodes :',len(G2.nodes()))
		display_graph(G2)
	plt.show()

def get_all_hot_songs(en,artists,G,liked_tracks):
	all_tracks = []
	popularity = []
	for artist in artists:
		N_songs = int(G.node[artist]['score'] / ratio_score_songs)
		response = en.get('song/search', artist_id =artist, results=2*N_songs,
						  bucket=['song_hotttnesss','id:spotify','tracks'], sort='song_hotttnesss-desc')['songs']
		last_titles = []
		k = 0
		found = 0
		while(k< len(response) and found < N_songs):
			song = response[k]
			if not(song['title'] in last_titles or song['title'] in liked_tracks):
				if(len(song['tracks']) > 0 and 'foreign_id' in song['tracks'][0] ):
					last_titles.append(song['title'])
					all_tracks.append(song['tracks'][0]['foreign_id'])
					popularity.append(song['song_hotttnesss'])
					found += 1
					print(song['title'],song['artist_name'])
				# else:
				# 	print('Oops, no spotify id')
			k += 1
	return(np.asarray(all_tracks)[np.argsort(popularity)[::-1]])


def add_new_tracks(new_tracks,username,token,to_playlist='ToDiscover'):
	sp = spotipy.Spotify(auth=token)

	# get 'liked' playlist
	playlists = sp.user_playlists(username)['items']
	playlist = None
	for p in playlists:
		if(p['name'] == to_playlist):
			to_playlist_id = p['id']

	for i in xrange(len(new_tracks)/100 +1):
		sp.user_playlist_add_tracks(username,to_playlist_id,new_tracks[(i*100):((i+1)*100)])
	print('Added ' + str(len(new_tracks)) + ' new tracks')