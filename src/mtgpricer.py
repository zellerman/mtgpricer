'''
Created on 2013.12.10.

@author: 502108836
'''
import os
import re

from readers import ParserFactory
import argparse
from datasources.editions import EditionMapper
from datasources.conditions import conditionMods, readConditions
from config.base import loadConfig
from config.logconfig import initLogging
from pricer import PriceCalculator
from formatter import FormatterFactory


class IOHandlers(object):
    pass


class SetHandlersAction(argparse.Action):
    def __call__(self, psr, namespace, values, option_string=None):
        print namespace
        print namespace.stock
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
                                              'Defalults are configurable and the fresh install has xx set.',
                        action=SetHandlersAction, default='xt')

    #force refresh DB
    parser.add_argument('-r', '--refreshdb', help='refresh the price database on startup (might take a few minutes)',
                        action='store_true')

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
    config = loadConfig('../res/mtgpricer.yaml')
    editionMapper = EditionMapper(config.get('staticdata').get('editions'))
    readConditions(config.get('staticdata').get('conditions'))
    handlers = IOHandlers()

    parser = setupParser()
    #a hack to always get SetHandlersAction called
    import sys
    if '-m' not in sys.argv and '--modes' not in sys.argv:
        sys.argv.append('-m')
        sys.argv.append('xx')
    parser.parse_args()

    cards = handlers.parser.parse()
    pc = PriceCalculator(conditionMods, {}, '')
    pricedCards = pc.calculateCardSet(cards)
    handlers.formatter.printCards(pricedCards)


