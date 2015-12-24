from artist_network import *
from song_db import *
from config import *

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import pickle
import sys

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

	return sp, p_name_id

def remove_from_playlist(track_id, from_playlist='ToDiscover'):
	sp, from_playlist_id = get_playlist(from_playlist)
	sp.user_playlist_remove_all_occurrences_of_tracks(username,
													  from_playlist_id,
													  [track_id])
	print 'Removed track from ' + from_playlist

def add_new_tracks(new_tracks,to_playlist='ToDiscover'):
	sp, to_playlist_id = get_playlist(to_playlist)
	for i in xrange(len(new_tracks)/100 +1):
		sp.user_playlist_add_tracks(username,
									to_playlist_id,new_tracks[(i*100):((i+1)*100)])
	print 'Added ' + str(len(new_tracks)) + ' new tracks'

def save_liked_artists(liked_artists):
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
	if not(title.lower() in history[id]):
		history[id].append(title.lower())

def get_liked_tracks(p_name='Liked',history={}, reset_db=False):
	token = login()

	if token:
		sp = spotipy.Spotify(auth=token)
		playlists = sp.user_playlists(username)['items']
		playlist = None
		for p in playlists:
			if(p['name'] == p_name):
				playlist = p

		liked_artists = set()
		if(playlist is None):
			print 'ERROR: could not find playlist ' + p_name
			sys.exit(1)

		results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
		tracks = results['tracks']
		df, history = add_likes(tracks, history)
		liked_artists.update([ item['track']['artists'][0]['name'] for item in tracks['items']])

		while tracks['next']:
			tracks = sp.next(tracks)
			df, history = add_likes(tracks, history, df)
			liked_artists.update([ item['track']['artists'][0]['name'] for item in tracks['items']])

		save_liked_artists(liked_artists)

		# save updated history
		output_file = open('history.csv', 'wb')
		pickle.dump(history,output_file)
		output_file.close()

		# save songdb
		if not(reset_db):
			df2 = pd.read_csv('song_db.csv', encoding='utf-8', index_col='track_id')
			df = df2.append(df)
		df.to_csv('song_db.csv', encoding='utf-8')

		return history

	else:
		print "ERROR: Cannot get token for " + username
		sys.exit(1)

def find_liked_artists(p_name='Liked'):
	token = login()

	if token:
		sp = spotipy.Spotify(auth=token)
		playlists = sp.user_playlists(username)['items']
		playlist = None
		for p in playlists:
			if(p['name'] == p_name):
				playlist = p

		liked_artists = set()
		if(playlist is None):
			print 'ERROR: could not find playlist ' + p_name
			sys.exit(1)

		results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
		tracks = results['tracks']
		liked_artists.update([ item['track']['artists'][0]['name'] for item in tracks['items']])
		while tracks['next']:
			tracks = sp.next(tracks)
			liked_artists.update([ item['track']['artists'][0]['name'] for item in tracks['items']])

		save_liked_artists(liked_artists)

	else:
		print "ERROR: Cannot get token for " + username
		sys.exit(1)