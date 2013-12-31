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
    print path

    entries = linesOfFile(path)
    for e in entries:
        k, v = striplist(map(lambda x: x.lower(), e.split(':')))
        conditionMods[k] = float(v)
        conditionNames.append(k)


if __name__ == '__main__':
    readConditions('../../res/conds')
    print conditionNames
