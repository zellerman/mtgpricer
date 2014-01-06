'''
Created on 2013.12.11.

@author: 502108836
'''
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, String, Float

Base = declarative_base()

from sqlalchemy.sql.expression import and_, func


class CardInfo(Base):
    __tablename__ = 'cardinfo'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    edition = Column(Unicode)
    rarity = Column(String)
    pic = Column(String)
    hi = Column(Float)
    med = Column(Float)
    lo = Column(Float)
    card = relationship("Card", uselist=False, backref="cardinfo")

    def __init__(self, name=None, edition=None, rarity=None, pic=None, hi=None, med=None, lo=None):
        self.name = name
        self.edition = edition
        self.rarity = rarity
        self.pic = pic
        self.hi = hi
        self.med = med
        self.lo = lo


    def tostring(self):
        return "[Card: " + ", ".join(
            filter(None, [self.name, self.edition, self.rarity, str(self.hi), str(self.med), str(self.lo)])) + "]"

    def __repr__(self):
        return self.tostring()

    def __str__(self):
        return self.tostring()

    def saveOrUpdate(self, session):
        dbEnt = session.query(CardInfo).filter(and_(func.lower(CardInfo.name) == func.lower(self.name),
                                                    func.lower(CardInfo.edition) == func.lower(self.edition))).first()
        if dbEnt:
            dbEnt.hi = self.hi
            dbEnt.med = self.med
            dbEnt.lo = self.lo
            session.merge(dbEnt)
            self = dbEnt
        else:
            session.add(self)


class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    condition = Column(String)
    info = Column(Integer, ForeignKey('cardinfo.id'))
    quantity = Column(Integer)
    price = Column(Float)


    def __init__(self, quantity=None, condition=None):
        self.condition = condition
        self.quantity = quantity

    def getattr(self, attr):
        if 'info' in attr:
            return getattr(self.info, attr[attr.index('.') + 1:])
        return getattr(self, attr)