'''
Created on 2013.12.10.

@author: 502108836
'''

from yaml import load
import logging



def loadConfig(path):
    try:
        with open(path) as f:
            config = load(f)
    except : 
        logging.error('Fatal error: Cannot load config, at {path}'.format(path=path))
        raise
    return config
