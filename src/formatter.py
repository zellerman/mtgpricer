'''
Created on 2013.12.20.

@author: 502108836
'''
import logging

import sys
import xlwt

logger = logging.getLogger('mine')


class FormatterFactory(object):
    @staticmethod
    def forCode(code, **kwargs):
        if code == 't':
            return BasicFormatter(kwargs['pricedstock'])
        if code == 'x':
            return ExcelFormatter(kwargs['pricedstock'],
                                  {'quantity': 0, 'info.name': 1, 'info.edition': 2, 'condition': 3, 'price': 4})


class BasicFormatter(object):
    def __init__(self, stream):
        self.stream = stream

    def printCards(self, cards):
        try:
            with open(self.stream, 'w') as dest:
                self.stream = dest
                for card in cards:
                    self.printCard(card)
        except Exception, e:
            print e.message
            logger.critical('Cannot save the results')

    def printCard(self, card):
        fmts = "{qty} {name} {ed} {cond} {pr}"
        print >> self.stream, fmts.format(qty=card.quantity, name=card.info.name,
                                          ed=card.info.edition, cond=card.condition, pr=card.price)
        self.echoCard(card)

    def echoCard(self, card):
        fmts = "{qty} {name} {ed} {cond} {pr}"
        print >> sys.stdout, fmts.format(qty=card.quantity, name=card.info.name,
                                         ed=card.info.edition, cond=card.condition, pr=card.price)


class ExcelFormatter(BasicFormatter):
    def __init__(self, workbook=None, headerOrder=None):
        self.workbook = workbook
        self.headerOrder = headerOrder
        self.sheet = None

    def printCards(self, cards):
        wb = xlwt.Workbook(encoding='utf-8')
        self.sheet = wb.add_sheet('stock')
        i = 1
        for card in cards:
            self.printCard(card, i)
            i += 1
            #cant save xlsx have to change the name if the input was xlsx
        if self.workbook.endswith('.xlsx'):
            self.workbook = self.workbook[0:-1]
        wb.save(self.workbook)

    def printCard(self, card, i):
        for name, col in self.headerOrder.iteritems():
            self.sheet.write(i, col, card.getattr(name))
        self.echoCard(card)

