from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

db_file_name = 'music.db'


engine = create_engine('sqlite:///%s' % db_file_name, echo=False)
db_session = scoped_session(sessionmaker(bind = engine))

def db_init():
	import model
	Base.metadata.create_all(bind = engine)
