'''
Created on 2013.12.20.

@author: 502108836
'''

import sys
class BasicFormatter(object):
    
    def __init__(self, stream=sys.stdout):
        self.stream=stream
        
    def printCards(self, cards):
        for card in cards:
            self.printCard(card)

    def printCard(self, card):
        fmts= "{qty} {name} {ed} {cond} {pr}"
        print >> self.stream, fmts.format(qty=card.quantity, name=card.info.name, 
                                          ed=card.info.edition, cond=card.condition, pr=card.price)
        pass
    