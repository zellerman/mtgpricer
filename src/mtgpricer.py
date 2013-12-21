'''
Created on 2013.12.10.

@author: 502108836
'''

import readers
from datasources.editions import EditionMapper
from datasources.conditions import conditionMods, conditionNames, readConditions
from config.base import loadConfig
from pricer import PriceCalculator
from formatter import BasicFormatter

if __name__ == '__main__':
    config= loadConfig('../res/mtgpricer.yaml')
    editionMapper = EditionMapper(config.get('staticdata').get('editions'))
    readConditions(config.get('staticdata').get('conditions'))
    cards = readers.readXLSStock('../test/stock.xlsx', editionMapper, conditionNames)
    pc = PriceCalculator(conditionMods, {}, '')
    pricedCards = pc.calculateCardSet(cards)
    BasicFormatter().printCards(pricedCards)
    