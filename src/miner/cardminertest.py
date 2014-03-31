import unittest
from sqlalchemy.sql.expression import and_
import priceminers
from datasources import database
from datasources.entities import CardInfo


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = database.DB('../../res/cards.db')

    @unittest.skip('fffag')
    def test1FetchRTR(self):
        """
            This test tries to fetch the page that contains the RTR listing.
            Exception during this operation is an instant fail.
            Also, if the result page fragment is empty, that means a fail due to
            layout changes or sth else.
        """
        try:
            htmlfrag = priceminers.fetchCardsFromPage('Return to Ravnica')
        except Exception, e:
            self.fail('Exception in getting the page!' + str(e))
        self.assertGreater(htmlfrag, 0, 'The fragment mined is empty!')

    @unittest.skip('fffag2')
    def test2CheckRTR(self):
        """
            This case checks wheter the basic card tokenizing works or not.
            The nr of card tr-s found or the rtr page should be 274. If the result
            differs, something has gone wrong. Either the page HTML has changed or else...
        """
        raw = priceminers.fetchCardsFromPage('Return to Ravnica')
        print raw
        self.assertEqual(len(priceminers.minecards(raw)), 274, 'Got fucked up??')

    def testPersistOnce(self):
        session = self.db.session
        ci = CardInfo(name=u'Talpak', edition=u'Uccu')
        ci2 = CardInfo(name=u'Talpak', edition=u'Uccu')
        ci.saveOrUpdate(session)
        ci2.saveOrUpdate(session)
        self.assertEqual(
            session.query(CardInfo).filter(and_(CardInfo.name == u'Talpak', CardInfo.edition == u'Uccu')).count(), 1,
            'It is not 1 bitch')

    def testUpdatePrice(self):
        session = self.db.session
        ci = CardInfo(name=u'Talpak8', edition=u'Uccu', lo=57)
        ci2 = CardInfo(name=u'Talpak8', edition=u'Uccu', lo=66)
        ci.saveOrUpdate(session)
        ci2.saveOrUpdate(session)
        self.assertEqual(
            session.query(CardInfo).filter(and_(CardInfo.name == u'Talpak8', CardInfo.edition == u'Uccu')).first().lo,
            66, 'Pricestuckman')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCheckRTR']
    unittest.main()