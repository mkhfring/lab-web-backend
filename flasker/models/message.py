
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy_media import File, MagicAnalyzer
from sqlalchemy_media.exceptions import ContentTypeValidationError


from .db import Base, session
from .types import Json


class FileAttachment(File):

    _internal_max_length = None

    _internal_min_length = None

    __pre_processors__ = [
        MagicAnalyzer(),
    ]


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    _attachment = Column(FileAttachment.as_mutable(JSON))
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    replied_id = Column(Integer, ForeignKey('message.id'))
    sender = relationship(
        'User',
        foreign_keys=[sender_id],
        backref='sent_messages'
    )
    receiver = relationship(
        'User',
        foreign_keys=[receiver_id],
        backref='received_messages'
    )
    reply_to = relationship(
        'Message',
        backref='parent_message',
        uselist=False,
        remote_side=id
    )
    created_at = Column(DateTime)

    @property
    def attachment(self):
        return self._attachment if self._attachment else None

    @attachment.setter
    def attachment(self, value):
        if value is not None:
            try:
                self._attachment = FileAttachment.create_from(value)

            except ContentTypeValidationError:
                raise Exception

    def __init__(self, title, body, create_at=None, reply_to=None):
        self.title = title
        self.body = body
        self.created_at = create_at
        self.reply_to = reply_to

