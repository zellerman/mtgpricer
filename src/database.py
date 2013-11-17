'''
Created on Mar 9, 2013

@author: davidborsodi
'''

import sqlalchemy
from sqlite3 import dbapi2 as sqlite

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData, Table, Unicode

path= '/Users/davidborsodi/Documents/googleappengine/mtgauction/mtgauction/cards.db'
engine = sqlalchemy.create_engine('sqlite:///'+path, module=sqlite)#, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
metadata = MetaData()


Base = declarative_base()

class CardInfo(Base):
    __tablename__ = 'cardinfo'
    
    id=Column(Integer, primary_key=True)
    name=Column(Unicode)
    edition=Column(Unicode)
    rarity=Column(String)
    pic=Column(String)
    hi=Column(Float)
    med=Column(Float)
    lo=Column(Float)
   
    def __init__(self, name=None, cost=None, edition=None, rarity=None,pic =None, hi=None, med=None, lo=None):
        self.name = name
        self.cost = cost
        self.edition = edition
        self.rarity = rarity
        self.pic = pic
        self.hi = hi
        self.med = med
        self.lo = lo
       
       
    def tostring(self):   
        return "[Card: " + ", ".join(filter(None,[self.name,  self.edition, self.rarity, str(self.hi), str(self.med), str(self.lo)])) + "]"
    def __repr__(self):
        return self.tostring()
    def __str__(self):
        return self.tostring()
    
ci = Table('cardinfo', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Unicode),
    Column('edition', Unicode),
    Column('rarity', String),
    Column('pic', String),
    Column('hi', Float),
    Column('med', Float),
    Column('lo', Float))


metadata.create_all(engine, checkfirst=True)


def save_list(entities):
    session.add_all(entities)
    session.commit()