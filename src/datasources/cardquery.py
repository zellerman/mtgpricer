'''
Created on 2013.12.09.

@author: 502108836
'''


import logging
import datasources
from sqlalchemy.sql.expression import func
from database import db
from entities import CardInfo

logger = logging.getLogger('mine')

def checkDB():
    #just a reasonably big enough number to ensure the db is not empty
    chkno = 500
    assert db.session.query(CardInfo).limit(chkno).count() == chkno


class CardFinder(object):
    """
        editions is a datasources.editions.EditionHandler object
        forceSingleMatch makes findCard return one match even if more is found. Defaulted to True.
    """

    def __init__(self, editions, forceSingleMatch=True):
        self.editions = editions
        self.forceSingleMatch = forceSingleMatch

    def findCard(self, card, edition=None):
        cquery = datasources.database.db.session.query(CardInfo).filter(func.lower(CardInfo.name) == func.lower(card))
        edition = self.getRealEditionName(edition)
        if edition is not None:
            cquery = cquery.filter(func.lower(CardInfo.edition) == func.lower(edition))
        cards = cquery.all()
        if not cards:
            logger.warn('not found: %s', card)
        if len(cards) > 1 and self.forceSingleMatch:
            logger.warn('more than one matches found for card: {card}, selecting first match: {ed}'.format(card=card,
                        ed=cards[0].edition))
            return cards[0:1]
        return cards

    #TODO this is still not good
    def findCards(self, cards, editions=None):
        print cards
        cards = map(lambda c: c.lower(), cards)
        cquery = db.session.query(CardInfo).filter(func.lower(CardInfo.name).in_(cards))
        if editions is not None:
            editions = map(self.getRealEditionName, editions)
            #    if editions is not None:
            #        cquery = cquery.filter(func.lower(CardInfo.edition)==func.lower(editions))
        cards = cquery.all();
        if not cards:
            logger.warn('not found any matching: %s', ' '.join(cards))
        return cards

    def getRealEditionName(self, ed):
        if ed is not None:
            return self.editions[ed.lower()]
        return None

    def isCardNamePrefix(self, prefix):
        return db.session.query(CardInfo).filter(func.lower(CardInfo.name).like(prefix + "%")).count() > 0


def allsets():
    sets = db.session.query(CardInfo.edition).distinct()
    for s in sets.all():
        print '{a}#{a},'.format(a=s[0])