'''
Created on Mar 7, 2013

@author: davidborsodi
'''

import xlwt, codecs, collections as co
from sqlalchemy.sql.expression import and_, func
from database import CardInfo, session

#CardKey=co.namedtuple('CardKey', ['name', 'edition'])
#

def read_stock(path, sm, fileout=None):
    lines = codecs.open(path, 'r', 'utf-8').readlines()
    stk =[]
    for line in lines:
        parts =line.split(';')
        qty = parts[0]
        name = parts[1].strip()
        edition = None
        if len(parts) > 2:
            edition = sm[parts[2].strip().lower()]
        cards = exact_name_lookup(name, edition)
        for card in cards:
            print qty, card.name, card.edition, card.hi, card.med, card.lo
            if fileout is not None:
                print >>fileout, qty, card.name, card.edition, card.hi, card.med, card.lo
                
        stk.append((qty, cards[0]))
    return stk

def read_stock_6th1(path, sm, fileout=None):
    lines = codecs.open(path, 'r', 'utf-8').readlines()
    stk =[]
    for line in lines:
        qty = 1
        name = line.strip()
        print name
        edition = sm['6th']
        cards = exact_name_lookup(name, edition)
        for card in cards:
            print qty, card.name, card.edition, card.hi, card.med, card.lo
            if fileout is not None:
                print >>fileout, qty, card.name, card.edition, card.hi, card.med, card.lo
                
        stk.append((qty, cards[0]))
    return stk
        
#    
#def read_cards(path):
#    cards = {}
#    reps = codecs.open(path, 'r', 'utf-8').readlines()
#    for rep in reps:
#        rep = rep[rep.index(':')+1:rep.index(']')]
#        parts = rep.split(',')
#        print parts
#        ck= CardKey(parts[0].strip(), parts[2].strip())
#        cards[ck]=(parts[4].strip(), parts[5].strip(), parts[6].strip())
#        
        

def partial_name_lookup(card, edition=None):
    pass
def exact_name_lookup(card, edition=None):
    cquery = session.query(CardInfo).filter(func.lower(CardInfo.name)==func.lower(card))
    if edition is not None:
        cquery = cquery.filter(func.lower(CardInfo.edition)==func.lower(edition))
    cards = cquery.all();    
    if cards == []:
        print 'not found:', card
    return cards[0:1]
    
#    hi, med, lo = 
#    return (card, edition, hi, med, lo)

#print session.query(CardInfo).filter(func.lower(CardInfo.name)==func.lower('stasis')).all()

def map_sets(sets):
    setmap = co.defaultdict()
    for ed in sets:
        ed = ed.strip()
#        print ed.split(';')
        name, abbrs = ed.split(';')
        name= name.lower()
        if ',' in abbrs:
            for abbr in abbrs.split(','):
                setmap[abbr.lower()] = name
        else:
            setmap[abbrs.lower()]=name
        setmap[name]=name
#    for k in setmap.iteritems():
#        print k
    return setmap
        
sm = map_sets(open('/Users/davidborsodi/mtgsets').readlines())
fout =open('krezganak', 'w+')
stk = read_stock_6th1('/Users/davidborsodi/krezgnak_6th', sm, fout)
fout.close()
#exit()
toloan = xlwt.Workbook(encoding='utf-8')
cardsheet = toloan.add_sheet('Items')
header = ['avail', 'lent', 'name', 'set', 'high', 'med','low'  ]

i = 0
while i < len(header):
    cardsheet.write(0, i, header[i])
    i+=1
    
line = 1
for st in stk:
    cardsheet.write(line, 0, st[0])
    card = st[1]
    cardsheet.write(line, 2, card.name)
    cardsheet.write(line, 3, card.edition.replace('+', ' '))
    cardsheet.write(line, 4, card.hi)
    cardsheet.write(line, 5, card.med)
    cardsheet.write(line, 6, card.lo)
    line +=1
    
toloan.save('./sul.xls')

    
    


