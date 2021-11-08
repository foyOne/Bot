from datetime import date
from sqlalchemy import Table, Column, Integer, ForeignKey, DATE, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.base import InPlaceGenerative
from sqlalchemy.sql.sqltypes import String

Base = declarative_base()

class Exercise(Base):
    __tablename__ = 'Exercise'

    Id = Column(Integer, primary_key=True)
    Date = Column(DATE, nullable=False)
    Name = Column(String(184), nullable=False)
    Sets = Column(Integer, nullable=False)
    Times = Column(Integer, nullable=False)
    Weight = Column(Integer, nullable=False)
    ChatId = Column(Integer, nullable=False)
    # ChatId = Column(Integer, ForeignKey('Chat.Id'))
    # Chat = relationship('Chat')

    @classmethod
    def GetActualFields(cls):
        return ['Date', 'Name', 'Sets', 'Times', 'Weight', 'ChatId']


# class Chat(Base):
#     __tablename__ = 'Chat'
    
#     Id = Column(Integer, primary_key=True)
#     Exercise = relationship('Exercise')