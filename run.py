from flask import Flask, flash, g, abort, render_template, session, request, redirect, url_for
from music.database import db_init, db_session
from music.model import Band, Album, Track, Genre, band_genre_table
import os, sqlalchemy
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import desc

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')



@app.route('/all/bands')
def show_bands():
	error = None
	try:
		bands = db_session.query(Band).order_by(Band.name)
	except NoResultFound:
		error = 'No bands at all in the database :('
	return render_template('show-band-list.html', error = error, band_list = bands)



@app.route('/all/albums')
def show_albums():
	error = None
	try:
		albums = db_session.query(Album).order_by(Album.name)
	except NoResultFound:
		error = 'No albums at all in the database :('
	return render_template('show-album-list.html', error = error, album_list = albums)



@app.route('/album/<int:album_id>')
def show_album(album_id):
	error = None
	try:
		album = db_session.query(Album).filter(Album.id == album_id).one()
		band = db_session.query(Band).filter(Band.id == album.band_id).one()
		tracks = db_session.query(Track).filter(Track.album_id == album_id)
	except NoResultFound:
		abort(404)
	return render_template('show-album.html', error = error, album = album, band_name = band.name, track_list = tracks, band_id = band.id)



@app.route('/band/<int:band_id>')
def show_band(band_id):
	error = None
	try:
		band = db_session.query(Band).filter(Band.id == band_id).one()
		albums = db_session.query(Album).filter(Album.band_id == band_id)

	except NoResultFound:
		abort(404)
	return render_template('show-band.html', error = error, band = band, albums = albums)



@app.route('/create/band', methods = ('GET', 'POST'))
def create_band():
	if request.method=='POST':
		band = Band(request.form['band_name'], request.form['start_year'],request.form['end_year'],request.form['origin'])
		
		db_session.add(band)
		db_session.commit()
		return redirect(url_for('show_bands'))
	else:
		return render_template('create-band.html')



@app.route('/delete/band/<int:band_id>', methods = ('GET', 'POST'))
def delete_band(band_id):
	if request.method=='POST':
		band = db_session.query(Band).filter(Band.id == band_id).one()
		db_session.delete(band)
		db_session.commit()
		return redirect(url_for('show_bands'))

	else:
		band = db_session.query(Band).filter(Band.id == band_id).one()
		return render_template('delete-band.html', band = band)



if __name__ == '__main__':
	app.run(debug = True)
