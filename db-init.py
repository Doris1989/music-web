from music.database import db_init, db_session
from music.model import Band, Album, Track, Genre

db_init()

band_data = open('bands.txt', 'r')

for line in band_data:
	tmp = line.split(',')
	band_name = tmp[0].strip()
	band_start_year = int(tmp[1].strip())
	band_last_year = tmp[2].strip()
	band_origin = tmp[3].strip()
	band = Band(band_name, band_start_year, band_last_year, band_origin)
	for item in tmp[4].split('.'):
		genre = Genre(item)
		band.genres.append(genre)
	db_session.add(band)

band_data.close()

album_data = open('albums.txt', 'r')
tmp = []
line = album_data.readline()
while line != '':

	if line[0]=='~':
		line = album_data.readline()							#read the '-' line
	elif line[0] == '@':
		line = album_data.readline()
	elif line[0] == '"':#read the trackline
		track_data = line.split('-')
		track_name = track_data[0]
		time = track_data[1].split(':')

		track_duration = int(time[0])*60+int(time[1])

		track = Track(track_name, track_duration)
		
		line = album_data.readline()
		album = db_session.query(Album).filter(Album.name == tmp[0]).one()
		track.album_id = album.id

		db_session.add(track)

	else:#this is a album data line, need to init the album table
		tmp = [s.strip() for s in line.split(',')]
		album_name = tmp[0]
		album_label = tmp[1]
		album_year = int(tmp[2])

		album = Album(album_name, album_year, album_label)
		

		line = album_data.readline()
		
		band = db_session.query(Band).filter(Band.name == tmp[3]).one()
		album.band_id = band.id
		
		db_session.add(album)

db_session.commit()


query = db_session.query(Band).join(Album).filter(Band.id == Album.band_id).filter(Album.label == 'Warp')
for band in query:
	print band.id, band.name 

query = db_session.query(Band).join(Album).join(Track).filter(Band.id == Album.band_id).filter(Album.id == Track.album_id).filter(Track.name == '"More Excuses"')
for band in query:
	print band.id, band.name 


