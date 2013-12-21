'''
Created on Mar 15, 2013

@author: davidborsodi
'''

'''
   PriceCalculator determines the price of a card given its database price and an optionally provided
   function.
   It can also change the price to other currencies if the mappings are given.
'''
class PriceCalculator:
    '''
        Conditions is the map of {condition - price scaler} values.
        Curs is the map of currencies in the format of {displayname - exchange rate relative to the base currency}
        Expr is the default pricer expression, if not given the median price is taken.
    '''
    def __init__(self, conditions, curs=None, expr=None):
        self.currencies=curs
        self.defaultExpression=expr
        self.conditions = conditions
        
    '''
        Returns the price of the in the currencies set for this PriceCalculator.
        Returns a map of currencyname-price pairs
    '''
    def otherCurrencies(self, price):
        returns = {'USD':price}
        if self.currencies and len(self.currencies) > 0:
            for c, rate in self.currencies.iteritems():
                returns[c] = price *rate
        return returns
        
    '''
        Calculates the price of the given card using the given expression.
        
        Takes a CardInfo object and an arithmetic expression.
        The expression - if given - must be a function of high(h), med(m) and low(l) prices or a constant, otherwise the price will be med.
        
        Returns the price as a real number. 
    '''
    def calcutatePrice(self, card, expression=None):
        h = card.hi
        m = card.med
        l = card.lo
        
        #avoid N/A problems in calculations
        if h < 0: h = 0.00001
        if m < 0: m = 0.00001
        if l < 0: l = 0.00001
        
        price = eval(expression) if expression else m
        return price
    
    #TODO if necessary
    def _evalpricer(self, h, l, m):
        pass

    '''
        Takes a set of Cards and prices them using the given pricing rules.
        Returns the cards with price info applied.
        The objects are modified in place.
        
        The algorithm is the following:
        1. Basic price is determined using the DB prices and the pricer function.
        2. Card condition is taken into account, using the predefined values.
        3. Total is calculated which is price * quantity
        4. If other currencies are given, the price (and the total is calculated in those as well)
        
    '''   
    def calculateCardSet(self, cards):
        for card in cards:
            card.price = self.calcutatePrice(card.info, self.defaultExpression)
            card.price = self.modulateByCondition(card.price, card.condition)
            card.prices = self.otherCurrencies(card.price)
        return cards

    def modulateByCondition(self, price, condition):
        return price*self.conditions[condition.lower()]
    
        
def calc_price(usd):
    if usd < 0.26:
        return 50
    elif usd < 0.51:
        return 100
    elif usd < 1.00:
        return 200
    else:
        return int(round(usd*200, -1))
def min_avg_mean(min, avg):
    return (min+avg)/2*225

fifty = []
hun = []
twohun = []
over =[]

def insert(cd, pr):
    if pr == 50:
        fifty.append((cd,str(pr)))
    elif pr ==100:
        hun.append((cd,str(pr)))
    elif pr == 200:
        twohun.append((cd,str(pr)))
    else:
        over.append((cd,str(pr)))
        
def ptlist(l):
    for e in l:
        print ' '.join(e)
        
def crappricer():
    cds = open('./crapp').readlines()
    
    total =0
    for cd in cds:
        pr = cd.split()[-1]
        bu = cd.split()[0:-3]
        total += calc_price(float(pr))
        insert(' '.join(bu),  calc_price(float(pr)))
    print '50/db'    
    ptlist(fifty)
    print '\n'    
    print '100/db'    
    ptlist(hun)
    print '\n'    
    print '200/db'    
    ptlist(twohun)
    print '\n'    
    print '200+'    
    ptlist(over)
    print 'EV: ', total    
    
def meanpricer(path):
    cds = open(path).readlines()
    
    total =0
    for cd in cds:
        min = cd.split()[-1]
        avg = cd.split()[-2]
        bu = cd.split()[0:-3]
        shog = min_avg_mean(float(min), float(avg))
        print ' '.join(bu), shog
        total += shog
    print total

#meanpricer('./krezganak')


    