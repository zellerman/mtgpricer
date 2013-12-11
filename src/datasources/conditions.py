'''
Created on 2013.12.11.

@author: 502108836
'''

from util import striplist, linesOfFile
conditionNames = []
conditionMods = {}

def readConditions(path):
    global conditionNames
    global conditionMods

    entries = linesOfFile(path)
    for e in entries:
        k,v = striplist(e.split(':'))
        conditionMods[k]=v
        conditionNames.append(k)

#readConditions('../../res/conds')        
    