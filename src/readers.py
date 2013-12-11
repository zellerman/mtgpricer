'''
This module holds various definitions to parse input sources
such as stock files.
Created on Apr 13, 2013

@author: davidborsodi

'''

import re
import collections as co
from _pyio import __metaclass__
import abc


def read_stock_defaulted(stockfile, defaultset):
    pass


def parse_stockfile(stockfile):
    pass
    
def setSeparator(self):
    if not re.search('[A-Z]+', self.lines[0]):
        self.separator = self.lines[0].strip()
        if len(self.separator) != 1:
            raise ValueError('Separator is too long')
    else:
        self.separator = ';'
    
    
'''
Constructs the set mapping from the input sequence.
Returns an map of setname=>[setname,abbrs...] for each entry.

The set mapping file should contain the abbreviations for set names.
Names are NOT case sensitive
Examples:
Type 1, without whitespaces in the entries
    Alpha: A
    Return to Ravniva: RTR 
    Tempest: TP TEP TMP

Type 2, with whitespaces in the entries a separator character is needed (comma!)
Duel Decks: Jace vs Chandra: DD jvc, DD:jvc,jvc
WPN Promos: p wpn, wpn


Two grammar options possible.

If the abbreviations don't contain whitespaces then:

    whitespace = "\s+";
    setname = "valid mtg setnames";
    abbr = "[^\s]+";
    entry = setname":"[whitespace][abbr]{[whitespace abbr]};
    grammar = { entry } ;
    
Otherwise you have to use a separator character:

    whitespace = "\s+";
    separator = ",";
    setname = "valid mtg setnames";
    abbr = "[^;]+";
    entry = setname":"[whitespace][abbr]{[separator abbr]};
    grammar = { entry } ;

'''


SEP=','
def readSetMap(sets):
    global SEP
    setmap = co.defaultdict()
    for ed in sets:
        ed = ed.strip()
        firstcolon = ed.index(':')
        name = ed[0:firstcolon]
        rest = ed[firstcolon+1:]
        separator = r'\s+'
        if SEP in rest:
            separator = SEP
        abbrs = map(lambda s: s.strip(), rest.split(separator))
        name= name.lower()
        for abbr in abbrs:
            setmap[abbr.lower()] = name
        setmap[name]=name
#    for k in setmap.iteritems():
#        print k
    return setmap
 
'''
Conform to the format:
[qty], [condition], [set], card

Quantity can be omitted, in this case the value is defaulted to 1.
Condition can be omitted in this case it is taken as NM.
If present it has to be a value from the predefined condition names.
By default the program identifies two condition sets:
GM-M-NM-EX-VG-G-P-HP
GM-M-NM-SP-MP-P-HP
+ and - is a syntactically valid modifier for any condition value (though might not make sense, like GM+)
BGS and PSA grade is also identified but subgrades are not for now.
i.e BGS9.5 is OK but BGS8(7.5,6,8.5,8.5) is not.

Set can be omitted, if the card is printed in only one set.
In any other cases the ambiguous result leads to a failed parse.

The separator can't be whitespace!
The default separator is comma, but a custom value can be defined in the first line of the file.
I this case that line should contain only that character and will be used as a separator.

'''       
def readPlainTextStock(stock):
    line0 = stock[0]
    separator = r'\s+'
    start = 0
    if len(line0.strip()) == 1:
        separator = ','
        start=1
    fields = ['qty', 'cond', 'set', 'card']
    cardsparsed = []
    for line in stock[start:]:
        line = re.sub(r'\s+', r' ', line)
        beg = 0
        carddata = []
        for field in fields:
            end = line.index(' ')
            val = line[beg:end]
            carddata.append((field, val))
            line = line[end+1:]
        carddata.append(('card', line))
        cardsparsed +=carddata
    return carddata
    
'''
Wut we know here is that 
the default separator is semicolon
set names, quantity and condition won't contain semicolon
and the premise have to be that the separator character can't be present in 
any of these.
the card name HAVE to be the last part of the line

So once we reach a point when qty set and cond is not matching, the
state must be cardparsing.
In the optimal case, the card name will be one token
Otherwise we'll just consume tokens until the last
if even with that, a cardname is not matched, we've got  parse error.

What can be an ambiguous parse?
-> the  token is valid in more than one category
    -> if the cardname is invalid, amend that token to the cardname
        -> this still won'solve all problems, e.g 
           line is ex, templar leader
           ex is a valid set and condition name
           templar leader is a valid card name
           ex, templar leader is a valid card name
           this clearly is a misparsed line with the default separator
        
If the separator character is a character that otherwise can appear in
one of the categories, ambiguous parses may occur. Avoid this.

'''    

MatchResult = co.namedtuple('MatchResult', 'matches token success')
class BasicMatchState(object):
    
    def __init__(self, fields, sets, conditions):
        self.fields = fields
        self.sets = sets
        self.conditions= conditions

    def match(self, token):
        matches = [getattr(self, field)(token) for field in self.fields]
        matchcount = matches.count(True)
        self.matchset = zip(self.fields, matches)
        if matchcount > 1:
            print 'Ambiguous parse, matches: {ms}'.format(ms=self.matchset)
            #raise Exception('Ambiguous parse, matches: {ms}'.format(ms=self.matchset))
        if matchcount < 1:
            self.transition = CardMatchState() 
            return self.transition.match(token)
        self.transition = self
        return MatchResult(self.matchset, token, True)

    def quantity(self, token):
        return token.isdigit()
        
    def setname(self, token):
        return token.lower() in self.sets
    
    def condition(self, token):
        return token.lower() in self.conditions or token.lower().startswith('bgs') or token.lower().startswith('psa')

    
class CardMatchState(object):
    
    def __init__(self,prevtoken=None):
        self.parts = []
        if prevtoken is not None:
            self.parts.append(prevtoken)
        self.transition = ()
        
    def match(self, token):
        self.parts.append(token)
        name= (' '.join(self.parts)).strip()
        for n in self.parts:
            print '%{n}%'.format(n=n)
        ismatch = self.checkCardExists(name)
        del self.parts[-1]
        self.parts.append(token+';')
        self.transition = self
        return MatchResult(('cardname',True),name, ismatch)

    def checkCardExists(self, cardname):
        cds = map(lambda x: x.strip(), open('../test/cards').readlines())
        return cardname in cds
#        pass  

class StockParser(object):
    
    def __init__(self, sets, conditions, lines, separator):
        self.separator = separator 
        self.fields = ['quantity', 'condition', 'setname']
        self.sets = sets
        self.conditions= conditions
        self.lines = lines

    def parse(self, tokens):
        if len(tokens) == 1:
            return (1, 'NM', '', tokens[0])
        terms =[]
        fields= self.fields[:]
        self.state = BasicMatchState(fields, self.conditions, self.sets)
        for token in tokens:
            term = self.state.match(token)
            terms.append(term)
            self.state = self.state.transition 
        return self.backtrack(terms)

    def backtrack(self, terms):
        fieldsToMatch = self.fields[:]
        fieldsToMatch.append('cardname')
        result = co.defaultdict(list)
        print '---------------------------'
        for term in terms:
            print '\t', term
        print '---------------------------'
        for ftm in fieldsToMatch:
            for term in terms:
                if term.success == True:
                    if (ftm, True) in term.matches:
                        result[ftm].append(term.token)
        print result
        return result
                
    def build(self):
        exprs = []
        for line in self.lines:
            line  = re.sub('\s+', ' ', line).strip()
            tokens = map(lambda x: x.strip(), line.split(self.separator))
            exprs.append(self.parse(tokens))
        return exprs

'''
Must have a header line
'''
   
import xlrd
import collections as co
def readXLSStock(stock):
    wb = xlrd.open_workbook(stock, ragged_rows=True)
    sheet= wb.sheet_by_index(0)
#    rowidx = -1 
#    rl = 0
#    while rl < 4:
#        rowidx+=1
#        rl = sheet.row_len(rowidx)
    keys = co.defaultdict(list)
    fieldcount = sheet.row_len(0)
    fields = {}
    for f in range(fieldcount):
        if sheet.cell_type(0, f) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
            pass
        else:
            fields[f] =  sheet.cell_value(0, f)
    print fieldcount
    rc = sheet.nrows
    print rc
    for rx in range(1, rc): 
        for colidx in range(sheet.row_len(rx)):
            print 'row', rx, 'col', colidx
            if sheet.cell_type(rx, colidx) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                pass
            else:
                keys[rx].append((colidx, sheet.cell_value(rx, colidx)))
                print sheet.cell_value(rx, colidx)
        
    

    