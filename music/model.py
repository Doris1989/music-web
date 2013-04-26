from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

band_genre_table = Table('band_genre', Base.metadata,
	Column('band_id', Integer, ForeignKey('band.id')),
	Column('genre_id', Integer, ForeignKey('genre.id'))

)

class Band(Base):
	__tablename__ = 'band'

	id        				= Column(Integer, primary_key=True)
	name      				= Column(String(1024))
	first_year_active = Column(Integer)
	last_year_active  = Column(Integer)
	place_of_origin   = Column(String(1024))

	albums = relationship('Album', backref = 'band')
	genres = relationship('Genre', secondary = band_genre_table, backref = 'band')

	def __init__(self, Name, First_year_active, Last_year_active, Place_of_origin):
		self.name 						 = Name
		self.first_year_active = First_year_active
		self.last_year_active  = Last_year_active
		self.place_of_origin   = Place_of_origin


class Album(Base):
	__tablename__='album'
  
	id       	    = Column(Integer, primary_key=True)
	name      	    = Column(String(1024))
	year_of_publication = Column(Integer)
	label         	    = Column(String(1024))
	band_id             = Column(Integer, ForeignKey('band.id'))

	album_track         = relationship('Track', backref = 'album')

	def __init__(self, Name, Year_of_publication, Label):
		self.name 							 = Name
		self.year_of_publication = Year_of_publication
		self.label 							 = Label


class Track(Base):
	__tablename__='track'

	id    	  = Column(Integer, primary_key=True)
	name  	  = Column(String(1024))
	duration  = Column(Integer)
	album_id  = Column(Integer, ForeignKey('album.id'))

	def __init__(self, Name, Duration):
		self.name		  = Name
		self.duration = Duration



class Genre(Base):
	__tablename__='genre'

	id   = Column(Integer, primary_key = True)
	name = Column(String(1024))

	def __init__(self, Name):
		self.name = Name




