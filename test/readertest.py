"""
Created on 2013.11.18.

@author: 502108836
"""
import unittest
from config.base import loadConfig
import datasources
from datasources.database import DB
from readers import StockParser, ExcelParser
from datasources.conditions import conditionNames, readConditions
from datasources.editions import EditionMapper
from config import logconfig

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logconfig.initLogging('../res/log.cfg')
        config = loadConfig('../res/mtgpricer.yaml')
        dbpath = config.get('staticdata').get('db')
        datasources.database.db = DB(dbpath)
        readConditions(config.get('staticdata').get('conditions'))
        cls.conditions = conditionNames
        cls.editions = EditionMapper('../res/sets')

    def tearDown(self):
        pass

    @unittest.skip("bobek")
    def testFindPart(self):
        tokens = ['1', 'overkill', 'force', 'natural', 'selection']
        sp = StockParser(self.conditions, self.editions, [], ' ')
        self.assertEquals(sp.findCardName(tokens), 'natural selection', 'fagness')

    def testXMLStock(self):
        config = loadConfig('../res/mtgpricer.yaml')

        dbpath = config.get('staticdata').get('db')
        datasources.database.db = DB(dbpath)
        print datasources.database.db
        stock = './stock.xlsx'
        ep = ExcelParser(stock, self.editions)
        ep.parse()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testReadPlaintTextStock']
    unittest.main()