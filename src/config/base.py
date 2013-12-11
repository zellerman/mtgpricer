'''
Created on 2013.12.10.

@author: 502108836
'''

import ConfigParser as CP
from ConfigParser import ConfigParser

def load(path):
    cp = ConfigParser()
    cp.read(path)
    return cp
