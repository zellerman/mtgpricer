'''
Created on 2013.12.21.

@author: 502108836
'''
import unittest


from datasources.cardquery import CardFinder
from datasources.editions import EditionMapper
class Test(unittest.TestCase):


    def setUp(self):
        self.singlefinder =CardFinder(EditionMapper('../res/sets'))
        self.multifinder =CardFinder(EditionMapper('../res/sets'), False)


    def tearDown(self):
        pass


    def testPrefixMatch(self):
        self.assertEquals(self.singlefinder.isCardNamePrefix('badlands'), True, '')
        self.assertEquals(self.singlefinder.isCardNamePrefix('holy day'), True, '')
        self.assertEquals(self.singlefinder.isCardNamePrefix('aglomberg'), False, '')
        self.assertEquals(self.singlefinder.isCardNamePrefix('tooth and'), True, '')
        self.assertEquals(self.singlefinder.isCardNamePrefix('force'), True, '')
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPrefixMatch']
    unittest.main()