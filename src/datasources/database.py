'''
Created on Mar 9, 2013

@author: davidborsodi
'''

from sqlalchemy import Column, Integer, String, Float, MetaData, Table, Unicode
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ForeignKey
from sqlite3 import dbapi2 as sqlite
import sqlalchemy


path= r'C:\opt\pydev\mtgpricer\src\cards.db'
engine = sqlalchemy.create_engine('sqlite:///'+path, module=sqlite)#, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
metadata = MetaData()

ci = Table('cardinfo', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Unicode),
    Column('edition', Unicode),
    Column('rarity', String),
    Column('pic', String),
    Column('hi', Float),
    Column('med', Float),
    Column('lo', Float))

c = Table('card', metadata, 
    Column('id',Integer, primary_key=True),
    Column('condition',String),
    Column('quantity', Integer),
    Column('price', Float),
    Column('info', Integer, ForeignKey('cardinfo.id'))
    )

metadata.create_all(engine, checkfirst=True)


def save_list(entities):
    session.add_all(entities)
    session.commit()