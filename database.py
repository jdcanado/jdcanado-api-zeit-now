#database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
engine = create_engine('sqlite:///' + os.path.join(basedir, 'db.apitruckpad')
def init_db():
  metadata.create_all(bind=engine)
