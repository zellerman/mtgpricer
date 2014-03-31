"""
Created on 2013.12.11.

@author: 502108836
"""
import re
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, String, Float

Base = declarative_base()

from sqlalchemy.sql.expression import and_, func


class Edition(Base):
    __tablename__ = 'edition'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    sexps = relationship("EditionSexp", backref="edition")
    cards = relationship("CardInfo", backref='edition')

    def __init__(self, name):
        self.name = name

    def tostring(self):
        return u"[Edition: " + u", ".join(
            filter(None, [self.name])) + u"]"

    def __repr__(self):
        return self.tostring()

    def __str__(self):
        return self.tostring()

    def save(self, session):
        dbEnt = session.query(Edition).filter(Edition.name == self.edition.name).first()
        if not dbEnt:
            session.add(self)


class EditionSexp(Base):
    __tablename__ = 'edition_sexp'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    source = Column(Unicode)
    ed_id = Column(Integer, ForeignKey('edition.id'))

    def __init__(self, name, src):
        self.name = name
        self.source = src


class IndividualPrice(Base):
    __tablename__ = 'individualprice'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    source = Column(String, nullable=False)
    cardinfo_id = Column(Integer, ForeignKey('cardinfo.id'))


class AvgPrice(Base):
    __tablename__ = 'avgprice'

    id = Column(Integer, primary_key=True)
    hi = Column(Float)
    med = Column(Float)
    lo = Column(Float)
    source = Column(String, nullable=False)
    cardinfo_id = Column(Integer, ForeignKey('cardinfo.id'))


class CardInfo(Base):
    __tablename__ = 'cardinfo'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    searchname = Column(Unicode)
    rarity = Column(String)
    edition_id = Column(Integer, ForeignKey('edition.id'))
    card = relationship("Card", backref="cardinfo")
    avgprices = relationship("AvgPrice",  backref="cardinfo")
    individualprices = relationship("IndividualPrice",  backref="cardinfo")

    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity
        self.searchname = re.sub('[^A-Za-z ]', '', name).lower()

    def tostring(self):
        return u"[Card: " + u", ".join(
            filter(None, [self.name, self.edition.name, self.rarity])) + u"]"

    def __repr__(self):
        return self.tostring()

    def __str__(self):
        return self.tostring()

    def save(self, session):
        dbEnt = session.query(CardInfo).join(Edition).filter(and_(func.lower(CardInfo.name) == func.lower(self.name),
                                                             Edition.name == self.edition.name)).first()
        if not dbEnt:
            session.add(self)


class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    condition = Column(String)
    cardinfo_id = Column(Integer, ForeignKey('cardinfo.id'))
    quantity = Column(Integer)
    price = Column(Float)

    def __init__(self, quantity=None, condition=None):
        self.condition = condition
        self.quantity = quantity

    def getattr(self, attr):
        if 'cardinfo' in attr:
            return getattr(self.info, attr[attr.index('.') + 1:])
        return getattr(self, attr)