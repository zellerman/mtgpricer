'''
Created on 2013.11.18.

@author: 502108836
'''
import unittest
from readers import StockParser, readXLSStock
from datasources.conditions import conditionNames
from datasources.editions import EditionMapper


class Test(unittest.TestCase):


    def setUp(self):
        self.conditions = conditionNames
        self.editions = EditionMapper('../res/sets')
    def tearDown(self):
        pass

    def testFindPart(self):
        tokens = ['1','overkill','force','natural','selection']
        sp = StockParser(self.conditions, self.editions, [], ' ')
        self.assertEquals(sp.findCardName(tokens), 'natural selection','fagness')

    @unittest.skip('fag')
    def testReadPlainTextStock(self):
        lines = map(lambda x: x.strip(), open('whitespacedstock').readlines())
        sp = StockParser(self.conditions, self.editions, lines, ' ')
        print lines
        ret = sp.build()
        for k in ret:
            print k
        pass
    
    @unittest.skip('pprop')
    def testReadXLSStock(self):
        filename = 'stock.xlsx'
        readXLSStock(filename)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testReadPlaintTextStock']
    unittest.main()