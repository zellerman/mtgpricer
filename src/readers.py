'''
This module holds various definitions to parse input sources
such as stock files.
Created on Apr 13, 2013

@author: davidborsodi

'''

import collections as co


def read_stock_defaulted(stockfile, defaultset):
    pass


def parse_stockfile(stockfile):
    pass
    
    
    
'''
Reads the set mapping file, if given.
The set mapping file should contain the abbreviations for set names.
E.g: 
Alpha: A
Return to Ravniva: RTR
'''
def readSetMap(sets):
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
        