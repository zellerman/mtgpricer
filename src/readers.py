'''
Module of stock parsers.

Created on Apr 13, 2013

@author: davidborsodi

'''

import re
import collections as co

from datasources.cardquery import CardFinder
from datasources.entities import Card
import logging

logger = logging.getLogger('mine')


def setSeparator(self):
    if not re.search('[A-Z]+', self.lines[0]):
        self.separator = self.lines[0].strip()
        if len(self.separator) != 1:
            raise ValueError('Separator is too long')
    else:
        self.separator = ';'


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
        start = 1
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
            line = line[end + 1:]
        carddata.append(('card', line))
        cardsparsed += carddata
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
        self.conditions = conditions

    def match(self, token, termmap):
        matched = False
        for field in self.fields:
            if getattr(self, field)(token):
                termmap[field].append(token)
                matched = True
        if not matched:
            raise Exception('Meaningless token: ', token)
        self.transition = self

    def quantity(self, token):
        return token.isdigit()

    def setname(self, token):
        return token.lower() in self.sets

    def condition(self, token):
        return token.lower() in self.conditions or token.lower().startswith('bgs') or token.lower().startswith('psa')


'''
a consecutive set of tokens which form a cardname
first and last token position in the parsed stream included
'''


class CardPart:
    def __init__(self, t, pos):
        self.tokens = [t]
        self.joined = t
        self.first = self.last = pos

    def addToken(self, t):
        self.tokens.append(t)
        self.joined += ' ' + t

    def __repr__(self):
        return '{t},<{f}:{l}>'.format(t=self.tokens, f=self.first, l=self.last)


class StockParser(object):
    #TODO: conform to the API
#    def __init__(self, stock, editionMapper, separator=';'):

    def __init__(self, editionMapper, conditions, lines, separator):
        self.separator = separator
        self.fields = ['quantity', 'condition', 'setname']
        self.editionMapper = editionMapper
        self.conditions = conditions
        self.lines = lines

    def parse(self, tokens):
        origtokens = tokens[:]
        try:
            if len(tokens) == 1:
                return 1, 'NM', '', tokens[0]
            termmap = co.defaultdict(list)
            cardname = self.findCardName(tokens)
            for token in tokens:
                self.state.match(token, termmap)
                self.state = self.state.transition
            self.consolidateTerms(termmap)
            termmap['name'] = cardname

        except Exception as e:
            logger.warning('Cannot parse row: %s', origtokens)
            logger.exception(e)
        return

    def consolidateTerms(self, termmap):
        pass

    def findCardParts(self, tokens, cf):
        cps = []
        contMatch = False
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if contMatch:
                print 'checking', cps[-1].joined + ' ' + token
                if cf.isCardNamePrefix(cps[-1].joined + ' ' + token):
                    cps[-1].addToken(token)
                    cps[-1].last = i
                else:
                    contMatch = False
                    i -= 1
            else:
                print 'checking', token
                if cf.isCardNamePrefix(token):
                    contMatch = True
                    cp = CardPart(token, i)
                    cps.append(cp)
            i += 1
        return cps

    '''
        Finds the card name in the token stream.
        Returns the card name and removes it from the tokens.
    '''

    def findCardName(self, tokens):
        cf = CardFinder(self.editionMapper)
        #populate the card parts, which is every word that is a prefix of a cardname
        cps = self.findCardParts(tokens, cf)
        #filter out partial matches
        candidates = []
        for cp in cps:
            if cf.findCard(cp.joined):
                candidates.append(cp)
                #if there is no match, we're fucked
        if not candidates:
            raise Exception('No card in the row: ' + ' '.join(tokens))
            #same is true for more than 3 results
        if len(candidates) > 3:
            raise Exception('Totally fucked up row: ' + ' '.join(tokens))

        #one match, coo
        if len(candidates) == 1:
            can = candidates[0]
            ll = len(tokens)
            tokens = tokens[:can.first]
            if can.last < ll - 1:
                tokens += tokens[can.last + 1:]
            return can.joined
            #if more than one candidates exists, cross check
        #first check whether any if them is a set name as well
        setnames = []
        for c in candidates:
            if self.editionMapper.isEdition(c.joined):
                setnames.append(c)
                #and check whether any of them is a condition name
        condnames = []
        for c in candidates:
            if c.joined in self.conditions:
                condnames.append(c)
                #if the previous lists are empty, there are two cards in the row..
        if setnames == [] and condnames == []:
            raise Exception('More than one card in the row:' + ' '.join(tokens))


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
                if term.success:
                    if (ftm, True) in term.matches:
                        result[ftm].append(term.token)
        print result
        return result

    def build(self):
        exprs = []
        for line in self.lines:
            line = re.sub('\s+', ' ', line).strip()
            tokens = map(lambda x: x.strip(), line.split(self.separator))
            exprs.append(self.parse(tokens))
        return exprs


'''
Must have a header line
'''

import xlrd
import collections as co


class ExcelParser(object):
    def __init__(self, stock, ed):
        self.stock = stock
        self.editionMapper = ed

    def parse(self):
        wb = xlrd.open_workbook(self.stock, ragged_rows=True)
        sheet = wb.sheet_by_index(0)
        raws = co.defaultdict(dict)
        fieldcount = sheet.row_len(0)
        fields = {}
        cf = CardFinder(self.editionMapper)
        for f in range(fieldcount):
            if sheet.cell_type(0, f) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                pass
            else:
                fields[f] = sheet.cell_value(0, f)
        print fieldcount
        rc = sheet.nrows
        print rc
        for rx in range(1, rc):
            for colidx in range(sheet.row_len(rx)):
                if sheet.cell_type(rx, colidx) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                    pass
                else:
                    raws[rx][fields[colidx]] = sheet.cell_value(rx, colidx)
        cards = []
        for rawCard in raws.values():
            c = Card(rawCard.get('qty', 1), rawCard.get('condition', 'NM'))
            cardInfo = cf.findCard(rawCard['name'], rawCard.get('set', None))
            if cardInfo:
                c.info = cardInfo[0]
                cards.append(c)
        print cards
        return cards


class RawCard(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.qty = kwargs.get('qty', 1)
        self.edition = kwargs.get('set', None)
        self.condition = kwargs.get('condition', None)

class ParserFactory(object):
    @staticmethod
    def forCode(code, **kwargs):
        if code == 't':
            pass
            #TODO return StockParser()
        if code == 'x':
            return ExcelParser(kwargs['stock'], kwargs['mapper'])
