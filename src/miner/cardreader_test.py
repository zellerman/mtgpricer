'''
Created on Dec 19, 2012

@author: davidborsodi
'''
import unittest
import cardreader

class Test(unittest.TestCase):

    '''
        This test tries to fetch the page that contains the RTR listing.
        Exception during this operation is an instant fail.
        Also, if the result page fragment is empty, that means a fail due to 
        layout changes or sth else.
    '''
    def test1FetchRTR(self):
        try:
            htmlfrag = cardreader.fetchCardsFromPage('Return to Ravnica')
        except Exception, e:
            self.fail('Exception in getting the page!' + str(e))
        self.assertGreater(htmlfrag, 0, 'The fragment mined is empty!')

    '''
        This case checks wheter the basic card tokenizing works or not.
        The nr of card tr-s found or the rtr page should be 274. If the result
        differs, something has gone wrong. Either the page HTML has changed or else...
    '''
    def test2CheckRTR(self):
        raw = cardreader.fetchCardsFromPage('Return to Ravnica')
        print raw
        self.assertEqual(len(cardreader.minecards(raw)), 274, 'Got fucked up??')
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCheckRTR']
    unittest.main()