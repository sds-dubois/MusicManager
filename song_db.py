from config import *
import pandas as pd
import numpy as np
import pickle

# limit_per_artist = 20
ratio_score_songs = 4

def update_opinion(track_id,o):
	df = pd.read_csv('song_db.csv', encoding='utf-8', index_col='track_id')
	df.set_value(track_id,'opinion',o)

def remember_song(song,history):
	id = song['artist_foreign_ids'][0]['foreign_id']
	if not(id in history):
		history[id] = []
	if not(song['title'].lower() in history[id]):
		history[id].append(song['title'].lower())
	return history

def add_likes(tracks, history, df1=None):
	df = pd.DataFrame()

	for item in tracks['items']:
		try:
			response = en.get('song/profile', track_id = item['track']['uri'],
							   results=1,
							   bucket=['song_hotttnesss','id:spotify','tracks','audio_summary']
							   )['songs']
			if(len(response) > 0):
				song = response[0]
				if(len(song['tracks']) > 0 and 'foreign_id' in song['tracks'][0]):
					# add to history
					history = remember_song(song,history)

					# add to songdb
					details = song['audio_summary']
					details.pop('analysis_url')
					details.pop('audio_md5')
					for key in ['song_hotttnesss','artist_name','artist_id','title']:
						details[key] = song[key]
					details['track_id'] = item['track']['uri']
					details['opinion'] = 1
					df = df.append(details, ignore_index=True)
		except:
			print 'WARNING: Could not find track\t' + item['track']['uri']

	df = df.set_index('track_id')
	if(df1 is not None):
		df = df1.append(df)
	return df, history

def get_new_suggestions(artists, G, history, reset=False):
	df = pd.DataFrame()
	new_tracks = []
	popularity = []
	for artist in artists:
		N_songs = int(G.node[artist]['score'] / ratio_score_songs)
		response = en.get('song/search', artist_id =artist, results=4*N_songs,
						  bucket=['song_hotttnesss','id:spotify','tracks','audio_summary'],
						  sort='song_hotttnesss-desc')['songs']
		k = 0
		found = 0
		while(k< len(response) and found < N_songs):
			song = response[k]
			if(len(song['tracks']) > 0 and 'foreign_id' in song['tracks'][0]):
				if not(song['artist_foreign_ids'][0]['foreign_id'] in history and
					   song['title'].lower() in history[song['artist_foreign_ids'][0]['foreign_id']]):
					# add to history
					history = remember_song(song,history)

					# add to songdb
					details = song['audio_summary']
					details.pop('analysis_url')
					details.pop('audio_md5')
					for key in ['song_hotttnesss','artist_name','title']:
						details[key] = song[key]
					details['artist_id'] = artist
					details['track_id'] = song['tracks'][0]['foreign_id']
					details['opinion'] = -1
					df = df.append(details, ignore_index=True)

					new_tracks.append(song['tracks'][0]['foreign_id'])
					popularity.append(song['song_hotttnesss'])
					found += 1
					print 'Adding :\t' + song['artist_name'] #+ ' \t ' + song['title']
			k += 1

	# update and save songdb
	df = df.set_index('track_id')
	if not(reset):
		df2 = pd.read_csv('song_db.csv', encoding='utf-8', index_col='track_id')
		df = df2.append(df)
	df.to_csv('song_db.csv', encoding='utf-8')

	# save new tracks & updated history
	ordered_new_tracks = np.asarray(new_tracks)[np.argsort(popularity)[::-1]]
	output_file = open('new_tracks.csv', 'wb')
	pickle.dump(ordered_new_tracks,output_file)
	output_file.close()
	output_file = open('history.csv', 'wb')
	pickle.dump(history,output_file)
	output_file.close()