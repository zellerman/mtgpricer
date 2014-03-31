"""
    Miner implementation for magiccards.info.
    tcgplayer sucks ass. anthologies no longer there? missing rarities. and a lot more.

"""
import logging
import os
import re
import requests
from requests.exceptions import HTTPError
from datasources import database
from datasources.entities import Edition
from miner.priceminers import CardParserBase
from util import linesOfFile

__author__ = '502108836'


logger = logging.getLogger('mine')


class TCGParser(CardParserBase):

    def __init__(self):
        os.environ['http_proxy'] = ''
        #TODO: make it configurable
        self.proxies = {
            #        "http": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
            # "https": "http://502108836:Alma%401234Alma@3.187.59.236:9400",
        }
        self.aggregateurl = 'http://magic.tcgplayer.com/db/price_guide.asp'
        self.individualurl = 'http://magic.tcgplayer.com/search_result.asp'
    def parseCardPage(self, cname):
        super(TCGParser, self).parseCardPage()
        params = {'name': cname, 'exact': '1'}

    def parseAggregatePage(self, setname):
        params = {'setname': setname}
        response = requests.get(self.aggregateurl, params=params)
        try:
            response.raise_for_status()
        except HTTPError, he:
            logger.exception("", he)
        tab = r'Low</font>\s*</td>.*?<TR(.*?)</table'
        cardpart = re.search(tab, response.text, re.DOTALL)
        print cardpart
        cardlist = cardpart.group(1).split(r'</TR>')
        for cardraw in cardlist:
            print cardraw
            pregex = r'<font\s+class=.*?>(.*?)[&nbsp;|]</font></td><td.*?><font\s+class=.*?>(.*?)[&nbsp;|]</font></td><td.*?><font\s+class=.*?>(.*?)[&nbsp;|]</font></td>'
            cp = re.search(pregex, cardraw)
            if cp:
                hi = cp.group(1)
                med = cp.group(2)
                lo = cp.group(3)
            else:
                logger.warning('match failed on line: ' + cardraw)
            # if not findexp:
            #     logger.warning('pattern failed to match on ' + cardraw)
            # href = findexp.group(1)
            # name = findexp.grup(2)
            # self.parseCardPage(href)


if __name__=='__main__':
    tp = TCGParser()
    tp.parseAggregatePage('alpha edition')