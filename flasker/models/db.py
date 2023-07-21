from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow


engine = create_engine('sqlite:///flasker.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
ma = Marshmallow()


def close_db(e=None):
    Base.metadata.drop_all(engine)
    print("The database is closed")





