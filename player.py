from my_utils import *
from config import *
from song_db import *

import sys


def save(track_id):
	# add to Liked playlist
	sp, liked_playlist_id = get_playlist('Liked')
	sp.user_playlist_add_tracks(username,
								liked_playlist_id,
								[track_id])	

	# add to history and songdb
	add_save_track(track_id)


def add(track_id):
	remove_from_playlist(track_id)
	sp, liked_playlist_id = get_playlist('Liked')
	sp.user_playlist_add_tracks(username,
								liked_playlist_id,
								[track_id])
	update_opinion(track_id,1)


def remove(track_id):
	remove_from_playlist(track_id)
	update_opinion(track_id,0)


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
	elif(action == 'save'):
		save(track_id)
	else:
		print 'ERROR: wrong action argument, should be like, pass, or save',sys.argv
		sys.exit(1)