'''
Created on 2013.12.10.

@author: 502108836
'''

from logging import config
import yaml


def initLogging(path):
    yf = open(path)
    lconf = yaml.safe_load(yf)
    config.dictConfig(lconf)