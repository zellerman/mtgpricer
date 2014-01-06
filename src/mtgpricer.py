'''
Created on 2013.12.10.

@author: 502108836
'''
import logging
import os
import re
import yaml
from miner import cardreader

from readers import ParserFactory
import argparse
from datasources.editions import EditionMapper
from datasources.conditions import conditionMods, readConditions
from datasources.database import DB
import datasources.database
from config.base import loadConfig
from config.logconfig import initLogging
from pricer import PriceCalculator
from formatter import FormatterFactory
from util import currentTimeMillis, dayToSec


class IOHandlers(object):
    pass


class SetHandlersAction(argparse.Action):
    def __call__(self, psr, namespace, values, option_string=None):
        #TODO no log entries here...
        global logger
        logger.debug(repr(namespace))
        logger.debug(namespace.stock)
        if namespace.overwrite:
            namespace.pricedstock = namespace.stock
        else:
            if not getattr(namespace, 'pricedstock'):
                try:
                    dotidx = namespace.stock.rindex('.')
                    namespace.pricedstock = namespace.stock[0:dotidx] + '_priced' + namespace.stock[dotidx:]
                except ValueError:
                    namespace.pricedstock = namespace.stock + '_priced'

        global handlers
        global editionMapper

        handlers.parser = ParserFactory.forCode(values[0], stock=namespace.stock, mapper=editionMapper)
        handlers.formatter = FormatterFactory().forCode(values[1], pricedstock=namespace.pricedstock)


def setupParser():
    parser = argparse.ArgumentParser()
    #mode switch
    parser.add_argument('-m', '--modes', help='Sets reader and formatter. Takes a two letter expression: "rf", where '
                                              'r is the reader code and f is the formatter code (x|t) '
                                              'Defaults are configurable and the fresh install has xx set.',
                        action=SetHandlersAction, default='xt')

    #force refresh DB
    parser.add_argument('-r', '--refreshdb', help='refresh the price database on startup (might take a few minutes)',
                        action='store_true', default=False)

    #in place pricing
    parser.add_argument('-o', '--overwrite', help='Overwrite the input file', action='store_true')

    #input file
    parser.add_argument('stock', help='the input stock file')

    #output file
    parser.add_argument('pricedstock', nargs='?',
                        help='the output destination for the priced stock, defaults to <stock>_priced.<ext> if not set')
    return parser


if __name__ == '__main__':
    initLogging('../res/log.cfg')
    logger = logging.getLogger('mine')
    config = loadConfig('../res/mtgpricer.yaml')
    editionMapper = EditionMapper(config.get('staticdata').get('editions'))
    dbpath = config.get('staticdata').get('db')
    datasources.database.db = DB(dbpath)
    readConditions(config.get('staticdata').get('conditions'))
    handlers = IOHandlers()

    progdata = loadConfig(config.get('staticdata').get('progdata'))

    parser = setupParser()
    #a hack to always get SetHandlersAction called
    import sys
    if '-m' not in sys.argv and '--modes' not in sys.argv:
        sys.argv.append('-m')
        sys.argv.append('xx')

    ns = parser.parse_args()
    refreshrate = dayToSec(config.get('vars').get('dbrefreshrate'))
    lastrefreshed = progdata.get('db').get('lastrefresh')
    now = currentTimeMillis()
    if ns.refreshdb or lastrefreshed < now - refreshrate:
        try:
            cardreader.processAll()
            progdata.get('db')['lastrefresh'] = now
            with open(config.get('staticdata').get('progdata'), 'w') as yaml_file:
                yaml_file.write(yaml.dump(progdata, default_flow_style=False))
        except Exception as e:
            logger.exception(e)

    cards = handlers.parser.parse()
    pc = PriceCalculator(conditionMods, {}, '')
    pricedCards = pc.calculateCardSet(cards)
    handlers.formatter.printCards(pricedCards)


