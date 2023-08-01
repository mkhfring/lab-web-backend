from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base, ma, session


class NewsCard(Base):
    __tablename__ = 'news_cards'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    
    def __init__(self, title):
        self.title = title
        
    @classmethod
    def get_news_fied(cls):
        fied = session.query(cls).one_or_none()
        return fied
    
    @classmethod
    def add_card(cls, card):
        session.add(card)
        session.commit()
        
        
    @classmethod
    def edit_card(cls, card, data):
        if type(data) is not dict:
            raise Exception('The input has to be a dictionary')
        
        for key,value in data.items():
            if hasattr(card, key):
                card.key = value
                setattr(card, key, value)
        
        session.commit()
        return card
        
        
    
class NewsItems(Base):
    __tablename__ = 'news_items'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    news_card_id = Column(Integer, ForeignKey('news_cards.id'))
    
    news_card = relationship(
        'NewsCard',
        foreign_keys=[news_card_id],
        backref='news_items'
    )
    
    def __init__(self, body):
        self.body = body
        
        
    @classmethod
    def get_news_list(cls):
        news_list = session.query(cls).all()
        return news_list
    
    @classmethod
    def add_news(cls, news):
        session.add(news)
        session.commit()
        
        
    @classmethod
    def edit_news(cls, id, body):
        news = session.query(cls).filter(cls.id == id).one_or_none()
        if not news:
            return news
        
        setattr(news, 'body', body)
        session.commit()
        return news
    
    @classmethod
    def delete_news(cls, id):
        news = session.query(cls).filter(cls.id == id).one_or_none()
        if news is None:
            return news
        
        session.delete(news)
        session.commit()
        return news
        
        
        
class NewsItemsSchema(ma.Schema):


    class Meta:
        fields = (
            "id",
            "body"
        )
        
        
class NewsCardSchema(ma.Schema):


    class Meta:
        fields = (
            "id",
            "title",
            "news_items"
        )