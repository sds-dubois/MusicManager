from artist_network import *
from song_db import *
from config import *

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import pickle

import pyen
import spotipy
import spotipy.util as util

def login(scope='user-library-read'):
    token = util.prompt_for_user_token(username, scope)    
    return(token)

def login_spotify_playlist():
	token = login('playlist-modify-public')
	sp = spotipy.Spotify(auth=token)

	if not(token):
		print 'ERROR: unable to log in Spotify'
		sys.exit(1)

	return sp

def get_playlist(p_name):
	sp = login_spotify_playlist()

	# get 'toDiscover' playlist
	playlists = sp.user_playlists(username)['items']
	p_name_id = None
	for p in playlists:
		if(p['name'] == p_name):
			p_name_id = p['id']

	if p_name_id is None:
		print 'ERROR: did not find playlist'
		sys.exit(1)

	return p_name_id

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
