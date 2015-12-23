from my_utils import *
from config import *

import sys

# def get_id(title,tracks):
# 	id_ = ''
# 	for item in tracks['items']:
# 		if(item['track']['name'] == title):
# 			id_ = item['track']['uri']
# 	return id_

# def remove_title_from_playlist(title, from_playlist='ToDiscover'):
# 	token = login('playlist-modify-public')
# 	sp = spotipy.Spotify(auth=token)

# 	if not(token):
# 		print 'ERROR: unable to log in Spotify'
# 		sys.exit(1)

# 	# get 'toDiscover' playlist
# 	playlists = sp.user_playlists(username)['items']
# 	from_playlist_id = None
# 	for p in playlists:
# 		if(p['name'] == from_playlist):
# 			from_playlist_id = p['id']

# 	if from_playlist_id is None:
# 		print 'ERROR: did not find playlist'
# 		sys.exit(1)

# 	# get track id
# 	results = sp.user_playlist(username, from_playlist_id, fields="tracks,next")
# 	tracks = results['tracks']
# 	id_ = get_id(title, tracks)
# 	while (id_ == '' and tracks['next']):
# 		tracks = sp.next(tracks)
# 		id_ = get_id(title, tracks)
# 	print id_

# 	if(id_ == ''):
# 		print 'ERROR: could not find track ' + title +' in ' + from_playlist
# 		sys.exit(1)
# 	else:
# 		sp.user_playlist_remove_all_occurrences_of_tracks(username, from_playlist_id, id_)
# 		print 'Removed track from ' + from_playlist

def remove_from_playlist(track_id, from_playlist='ToDiscover'):
	from_playlist_id = get_playlist(from_playlist)
	sp.user_playlist_remove_all_occurrences_of_tracks(username,
													  from_playlist_id,
													  [track_id])
	print 'Removed track from ' + from_playlist


def add(track_id):
	remove_from_playlist(track_id)
	liked_playlist_id = get_playlist('Liked')
	sp.user_playlist_add_tracks(username,
								liked_playlist_id,
								[track_id])
	# ToDo: update song_db


def remove(track_id):
	remove_from_playlist(track_id)
	# ToDo: update song_db


if __name__ == '__main__':

	if(len(sys.argv) != 3):
		print 'ERROR: wrong number of arguments', sys.argv
		sys.exit(1)

	action = sys.argv[1]
	track_id = sys.argv[2]

	if(action == 'like'):
		add(track_id)
	elif(action == 'pass'):
		remove(track_id)
	else:
		print 'ERROR: wrong action argument, should be like or pass',sys.argv
		sys.exit(1)