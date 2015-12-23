from my_utils import *
from config import *

import sys


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