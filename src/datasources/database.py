from sqlalchemy import Column, Integer, String, Float, MetaData, Table, Unicode
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ForeignKey
from sqlite3 import dbapi2 as sqlite
import sqlalchemy

#TODO this whole thing smells but right now I want a release
db = None


class DB(object):
    def __init__(self, path):
        self.engine = sqlalchemy.create_engine('sqlite:///' + path, module=sqlite)  #, echo=True)

        Session = sessionmaker()
        Session.configure(bind=self.engine)

        self.session = Session()
        metadata = MetaData()

        ci = Table('cardinfo', metadata,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('name', Unicode),
                   Column('edition', Unicode),
                   Column('rarity', String),
                   Column('pic', String),
                   Column('hi', Float),
                   Column('med', Float),
                   Column('lo', Float)
        )

        c = Table('card', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('condition', String),
                  Column('quantity', Integer),
                  Column('price', Float),
                  Column('info', Integer, ForeignKey('cardinfo.id'))
        )

        metadata.create_all(self.engine, checkfirst=True)

    def save_list(self, entities):
        self.session.add_all(entities)
        self.session.commit()

