from sqlalchemy import Column, Integer, String, ForeignKey
from .db import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    body = Column(String)


