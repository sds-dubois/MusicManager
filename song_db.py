import pandas as pd
limit_per_artist = 20

def populate_db(artists,en,reset=False):
	df = pd.DataFrame()
	for artist in artists:
		print('search',artist)
		response = en.get('song/search', artist_id =artist, results=limit_per_artist,
						  bucket=['song_hotttnesss','id:spotify','tracks','audio_summary'], sort='song_hotttnesss-desc')['songs']
		for song in response:
			if(len(song['tracks']) > 0 and 'foreign_id' in song['tracks'][0] ):
				details = song['audio_summary']
				details.pop('analysis_url')
				details.pop('audio_md5')
				for key in ['song_hotttnesss','artist_name','title']:
					details[key] = song[key]
				details['artist_id'] = artist
				details['track_id'] = song['tracks'][0]['foreign_id']
				details['opinion'] = -1
				df = df.append(details, ignore_index=True)
				print(song['title'],song['artist_name'])
	df = df.set_index('track_id')
	if not(reset):
		df2 = pd.read_csv('song_db.csv', encoding='utf-8')
		df2 = df2.set_index('track_id')
		df = df2.append(df)
	df.to_csv('song_db.csv', encoding='utf-8')