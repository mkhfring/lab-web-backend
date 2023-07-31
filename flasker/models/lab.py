from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base, ma, session


class Lab(Base):
    __tablename__ = 'lab'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(String)
    
    def __init__(self, summary, title):
        self.title = title
        self.summary = summary
        
    @classmethod
    def get_lab(cls):
        lab = session.query(cls).one_or_none()
        return lab
    
    @classmethod
    def add_lab(cls, lab):
        session.add(lab)
        session.commit()
        
    @classmethod
    def edit_lab(cls, lab, data):
        if type(data) is not dict:
            raise Exception('The input has to be a dictionary')
        
        for key,value in data.items():
            if hasattr(lab, key):
                lab.key = value
                setattr(lab, key, value)
        
        session.commit()
        return lab
        

class LabSchema(ma.Schema):


    class Meta:
        fields = (
            "id",
            "title",
            "summary"
        )