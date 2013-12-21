'''
Created on 2013.12.11.

@author: 502108836
'''
import unittest

import datasources.editions as edsource
from config import logconfig

logconfig.initLogging('../res/log.cfg')
class Test(unittest.TestCase):


    def testInit(self):
        eh= edsource.EditionMapper('../res/sets')
        #cherry pick some to randomly test
        self.assertEqual("Alpha Edition", eh['a'], "Tim is gay"+eh['a'])
        self.assertEqual("Arabian Nights", eh['Arabian Nights'], "Tim is gay"+eh['a'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()