"""
Created on Dec 19, 2012

@author: davidborsodi
"""
import logging
import os
import re
import codecs
from HTMLParser import HTMLParser

import requests
from requests.packages.urllib3.exceptions import HTTPError

from datasources import database
from datasources.entities import CardInfo
from util import striplist, strip_accents

logger = logging.getLogger('mine')


class Requestor(object):

    def gethttp(self, **kwargs):
        url = kwargs['url']
        del kwargs[url]
        response = requests.get(url, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError, he:
            logger.exception("", he)


class CardParser:
    def __init__(self):
        self.currentCard = None

    def parse(self, raw):
        TRS_TOK = '<tr>'
        TRE_TOK = '</tr>'
        TE_LEN = len(TRE_TOK)
        cards = []
        start = 0
        #        print raw
        while start >= 0:
            start = raw.find(TRS_TOK)
            if start < 0:
                break
            raw = raw[start:]
            end = raw.find(TRE_TOK)
            self.processProps(raw[0:end + TE_LEN])
            cards.append(self.currentCard)
            raw = raw[end + TE_LEN:]
        return cards

    def processProps(self, raw):
        fields = ['Name', 'Cost', 'Edition', 'Rarity', 'High', 'Med', 'Low']
        TDS_TOK = '<td'
        TDE_TOK = '</td>'
        TDE_LEN = len(TDE_TOK)
        i = 0
        self.currentCard = CardInfo()
        while i < len(fields):
            start = raw.find(TDS_TOK)
            if start >= 0:
                end = raw.find(TDE_TOK)
                if end < 0:
                    print 'Got fucked'
                    continue
                    #                print raw[start:end+TDE_LEN]
                self.mineNext(raw[start:end + TDE_LEN], fields[i])
                raw = raw[end + TDE_LEN:]
                #                print raw
                i += 1

                #        print self.currentCard

    def mineNext(self, rawProp, prop):
    #        print rawProp
        miner = getattr(self, 'mine' + prop)
        try:
            miner(rawProp)
        except Exception as e:
            print 'Exception in call to {0} with the following raw data: {1} '.format(miner, rawProp)
            print e
        pass

    def mineName(self, rawProp):
        namecontent = self.mineTDContent(rawProp)
        raw = re.search(r'\?cn=(.*)&', namecontent).group(1)
        unic = strip_accents(raw.decode('utf8'))
        #        print 'orig ', raw
        #        print 'deciso ', raw.decode('iso-8859-1')
        #        print 'decut ', raw.decode('utf8')
        #        print 'denorm', strip_accents(unic)
        #        print 'decue ', raw.decode('unicode-escape')

        self.currentCard.name = unic

    def mineHigh(self, rawProp):
        con = self.mineDeepTag(rawProp)
        if con[0] == '$':
            con = con.replace(',', '')
            self.currentCard.hi = float(con[1::])
        else:
            self.currentCard.hi = -1

    def mineMed(self, rawProp):
        con = self.mineDeepTag(rawProp)
        if con[0] == '$':
            con = con.replace(',', '')
            self.currentCard.med = float(con[1::])
        else:
            self.currentCard.med = -1

    def mineLow(self, rawProp):
        con = self.mineDeepTag(rawProp)
        if con[0] == '$':
            con = con.replace(',', '')
            self.currentCard.lo = float(con[1::])
        else:
            self.currentCard.lo = -1

    def mineCost(self, rawProp):
        self.currentCard.cost = self.mineTDContent(rawProp)

    def mineEdition(self, rawProp):
        edcontent = self.mineTDContent(rawProp)
        self.currentCard.edition = self.mineDeepTag(edcontent)

    def mineRarity(self, rawProp):
        self.currentCard.rarity = self.mineTDContent(rawProp)

    @staticmethod
    def mineDeepTag(tag):
        deepest = re.search(r'<[^>]*?>([^<]+|<(?![^>]*?>))</[^>]*?>', tag).group(1)
        if '<' in deepest:
            tc = re.search(r'<.*?>(.*)<', deepest).group(1)
            return tc
        return deepest

    @staticmethod
    def mineTDContent(td):
        tdc = re.search(r'<td[^>]*>(.*)</td>', td).group(1)
        return tdc

    def minePic(self, rawProp):
        pass


def fetchCardsFromPage(setname):
    results = requests.get("http://magic.tcgplayer.com/db/search_result.asp",
                           params={'Set_Name': setname}, timeout=10)
    pagetext = re.sub(r'(\n|\t|\r)', '', results.text.encode('utf-8'))
    print 'sn', setname
    cardsraw = re.search(r'ACTION="search_result.asp"(.*)</table></FORM>', pagetext, re.MULTILINE | re.DOTALL)
    print cardsraw
    return cardsraw.group(1)


def fetchAll(setnames, output):
    for setname in setnames:
        raw = fetchCardsFromPage(setname)
        cards = CardParser().parse(raw)
        # save_list(cards)
        for card in cards:
            card.saveOrUpdate(database.db.session)
        database.db.session.commit()
        for z in cards:
            print >> output, z


def getSets():
    os.environ['http_proxy'] = ''
    proxies = {
        #        "http": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
        # "https": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
    }
    results = requests.get("http://store.tcgplayer.com/magic", proxies=proxies, params={'partner': 'MTGTCG'},
                           timeout=10)
    print results.text
    flop = re.search(r'<select id="SetName"\s+name="SetName"\s+style="">(.*?)</select>', results.text, re.DOTALL)
    setsraw = flop.group(1).strip()
    setnames = []
    hp = HTMLParser()
    print setsraw
    for st in striplist(setsraw.split(r'option>')):
        print 'stmax', st
        rawElem = re.search(r'>(.*?)</', st)
        if rawElem:
            setname = hp.unescape(rawElem.group(1))
            print setname
            setnames.append(setname)
    setnames.remove('All Sets')
    return setnames


def processAll():
    setnames = getSets()
    cardsfile = codecs.open('cards', 'w+', 'utf-8')
    fetchAll(setnames, cardsfile)
    cardsfile.close()


class CardParserBase(object):

    def parse(self, sets):
        """
        Api entry
        @return:
        """
        pass

    def parseCardPage(self, name):
        #db/search_result.asp?name=armageddon&exact=1
        """
        Parser of the individual card page, if applicable
        @return:
        """
        pass

    def parseAggregatePage(self, edition):
        """
        Parser of the card aggregator page (e.g set page) if applicable.
        @return:
        """
        pass


class Miner(object):

    def __init__(self, cardparser, host):
        """
        @param cardparser: parser for the site
        @param host: the host url
        """
        self.host = host
        self.cardparser = cardparser
        self.setnames = None

    def processAll(self):
        self.getSets()
        self.fetchAll()

    def getSets(self):
        """
        set names are always mined from the same, trusted source: magiccards.info
        @return:
        """
        os.environ['http_proxy'] = ''
        proxies = {
            #        "http": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
            # "https": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
        }
        results = requests.get("http://magiccards.info/search.html", proxies=proxies,
                               timeout=10)
        # print results.text
        setstag = re.search(r'<label\s+for="edition">.*?<option value=""></option>(.*?)</select>', results.text, re.DOTALL)

        setsraw = setstag.group(1).strip()
        # print setsraw
        setnames = []
        hp = HTMLParser()
        print setsraw
        for st in striplist(setsraw.split(r'option>')):
            print 'stmax', st
            rawElem = re.search(r'value="(.*)">(.*?)<', st)
            if rawElem:
                setkey = hp.unescape(rawElem.group(1))
                setname = hp.unescape(rawElem.group(2))
                print setkey, setname
                setnames.append(setname)
        setnames.remove('All Sets')
        self.setnames = setnames

    def fetchAll(self):
        pass

if __name__ == '__main__':
    database.db = database.DB('../../res/cards.db')
    m = Miner('')
    m.getSets()
    #getSets()
    # processAll()
