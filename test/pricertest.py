'''
Created on 2013.12.09.

@author: 502108836
'''
import unittest
import pricer
from pricer import PriceCalculator

from datasources.cardquery import CardFinder
from datasources.editions import EditionHandler
from datasources.conditions import conditionMods, readConditions

import config.logconfig as lc


class Card:
    
    def __init__(self, n, e=None):
        self.name=n
        self.edition=e
        
    def __repr__(self):
        return '{n}, {e}'.format(n= self.name, e=self.edition)
    
    pass



class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        lc.initLogging('../res/log.cfg')
        self.pc = PriceCalculator({'EX':0.8, 'NM':1}, {'HUF', 220}, '(h+l)/2')
        self.cf = CardFinder(EditionHandler('../res/sets'))
        readConditions('../res/conds')


    def tearDown(self):
        pass


    def testLookup(self):
        c = Card('badlands')
        print self.cf.findCard(c.name )
        pass

    def testLookupAll(self):
        c = Card('badlands')
        c2 = Card('foil')
        c3 = Card('timetwister')
        print 'cucc', [c, c2]
        
        print self.cf.findCards([c.name, c2.name, c3.name])
        
    def testCalculatePrice(self):
        c = Card('badlands', 'revised edition')
        info = self.cf.findCard(c.name, c.edition )[0]
        print info
        pc =pricer.PriceCalculator(conditionMods)
        self.assertAlmostEqual(58.55,  pc.calcutatePrice(info, '(m+l)/2'))
        
    def testCalculateCardSet(self):
        pass
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLookup']
    unittest.main()