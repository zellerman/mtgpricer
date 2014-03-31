import unittest
from config import logconfig
from config.base import loadConfig
import datasources
from datasources.database import DB
from datasources.entities import CardInfo, Edition

__author__ = '502108836'


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logconfig.initLogging('../res/log.cfg')
        dbpath = '../res/expdb.db'
        cls.db = datasources.database.db = DB(dbpath)

    def testCheckSets(self):
        res = self.db.session.query(Edition).order_by(Edition.name).all()
        for e in res: print e

    def testcheckNrOfCards(self):
        res = self.db.session.query(CardInfo).join(Edition).filter(Edition.name == 'Dark Ascension').all()
        self.assertEqual(len(res), 171)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()