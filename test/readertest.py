'''
Created on 2013.11.18.

@author: 502108836
'''
import unittest
from readers import StockParser, readXLSStock


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


#    def testReadPlainTextStock(self):
#        lines = map(lambda x: x.strip(), open('whitespacedstock').readlines())
#        print lines
#        sp = StockParser(['a','b','u','rav', 'ex'], ['ex','gm','f','p'], lines, ';')
#        ret = sp.build()
#        for k in ret:
#            print k
#        pass
    
    def testReadXLSStock(self):
        filename = 'stock.xlsx'
        readXLSStock(filename)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testReadPlaintTextStock']
    unittest.main()