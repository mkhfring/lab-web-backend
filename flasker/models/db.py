import os
import functools

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow

from sqlalchemy_media import  StoreManager, FileSystemStore

from ..config import TestingConfig, DeploymentConfig


if os.getenv('MODE') == 'deployment':
        cfg = DeploymentConfig()
else:
        cfg = TestingConfig()
        
engine = create_engine(cfg.DBURL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
ma = Marshmallow()

base_url = 'http://localhost:5000/assets'
TEMP_PATH = '/tmp/sqlalchemy-media'

StoreManager.register(
        'fs',
        functools.partial(FileSystemStore, TEMP_PATH, base_url),
        default=True
)

def close_db(e=None):
    Base.metadata.drop_all(engine)
    print("The database is closed")





