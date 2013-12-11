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
        edsource.EditionHandler('../res/sets')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()