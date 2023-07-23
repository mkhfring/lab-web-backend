from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from sqlalchemy_media import File


from .db import Base, session, ma


class FileAttachment(File):

    _internal_max_length = None

    _internal_min_length = None


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    title = Column(String)
    description = Column(String)
    _avatar = Column(FileAttachment.as_mutable(JSON))

    def __init__(self, password, first_name, last_name, title, description, email=None):

        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.title = title
        self.description = description


    @classmethod
    def get_member(cls, email):
        member = session.query(cls).filter(
            cls.email == email
        ).one_or_none()
        return member

    @classmethod
    def add_member(cls, user):
        session.add(user)
        session.commit()

    @classmethod
    def get_member_by_id(cls, user_id):
        return session.query(cls).filter(
            cls.id == int(user_id)
        ).one_or_none()
        
    @property
    def avatar(self):
        return self._avatar if self._avatar else None

    @avatar.setter
    def avatar(self, value):
        if value is not None:
            try:
                self._avatar = FileAttachment.create_from(value)

            except ContentTypeValidationError:
                raise Exception

class UserSchema(ma.Schema):


    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "title",
            "description"
        )

