from HTMLParser import HTMLParser
import logging
import os
import re
import requests
import select
from sqlalchemy import and_, func
from sqlalchemy.exc import IntegrityError
from datasources import database
from util import striplist, strip_accents

__author__ = '502108836'

logger = logging.getLogger('mine')

from datasources.entities import CardInfo, Edition, EditionSexp


class DBPopulator(object):
    """
    This class reads magiccards.info and saves all cards found info the database.
    """

    def __init__(self, db):
        os.environ['http_proxy'] = ''
        #TODO: make it configurable
        self.proxies = {
            #        "http": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
            # "https": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
        }
        self.db = db

    def buildDB(self):
        sets = self.getSets()
        for edition in sets:
            self.getCards(edition)

    def getSets(self):
        """
        @return: Set names found
        """
        results = requests.get("http://magiccards.info/search.html", proxies=self.proxies,
                               timeout=10)
        # print results.text
        setstag = re.search(r'<label\s+for="edition">.*?<option value=""></option>(.*?)</select>', results.text,
                            re.DOTALL)

        setsraw = setstag.group(1).strip()
        setnames = []
        hp = HTMLParser()
        print setsraw
        for st in striplist(setsraw.split(r'option>')):
            print 'stmax', st
            rawElem = re.search(r'value="(.*)">(.*?)<', st)
            if rawElem:
                setkey = hp.unescape(rawElem.group(1))
                setname = hp.unescape(rawElem.group(2))
                if not self.db.session.query(Edition).filter(Edition.name == setname).count():
                    ed = Edition(setname)
                    ed.sexps.append(EditionSexp(setkey, 'http://magiccards.info'))
                    ed.save(self.db.session)
                    print setkey, setname
                    setnames.append(setname)
        try:
            self.db.session.commit()
        except IntegrityError as ie:
            print ie.message
            logger.severe('', ie)

        return setnames

    def getCards(self, edition, edkey):
        qs = 'e:{k}'.format(k=edkey)
        # response = requests.get('http://magiccards.info/'+edkey, params={'q': qs, 'v': 'list'}, proxies=self.proxies)
        response = requests.get('http://magiccards.info/'+edkey+'.html', proxies=self.proxies)
        text = response.text.replace('\n', '')
        print text
        tab = '<th><b>Edition</b></th>\s+</tr>(.*?)</table>'
        cardpart = re.search(tab, text, re.DOTALL)
        print cardpart
        cardlist = cardpart.group(1).split(r'</tr>')
        for cardraw in cardlist:
            findexp = re.search(r'<a\s+href="(.*?)">(.*?)</a>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',
                                cardraw, re.DOTALL)  # cardpage, name, type, cc, rarity
            if not findexp:
                logger.warning('pattern failed to match on "' + cardraw + '"')
                print 'pattern failed to match on "' + cardraw + '"'
                continue
            name = findexp.group(2)
            print name
            print 'orig ', type(name)
            # print 'deciso ', name.decode('iso-8859-1')
            # print 'decut ', name.decode('utf8')
            name = strip_accents(name)
            print name
            rarity = findexp.group(5)
            print rarity
            ci = CardInfo(name, rarity)
            ci.edition = self.db.session.query(Edition).filter(Edition.name == edition).first()
            ci.save(self.db.session)
        self.db.session.commit()


if __name__ == '__main__':
    database.db = database.DB('../../res/expdb.db')
    dbp = DBPopulator(database.db)
    #dbp.getSets()
    eds = database.db.session.query(Edition).all()
    for ed in eds:
        sexp = filter(lambda a: a.source == 'http://magiccards.info', ed.sexps)[0]
        print ed.name, sexp.name
        if database.db.session.query(CardInfo).join(Edition).filter(Edition.name == ed.name).count() < 1:
            dbp.getCards(ed.name, sexp.name)
    # dbp.getCards('Arena League', 'arena/en')