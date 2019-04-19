#database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
engine = create_engine('sqlite:///' + os.path.join(basedir, 'db.apitruckpad')
#metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))                       
                       
#def init_db():
#  metadata.create_all(bind=engine)
