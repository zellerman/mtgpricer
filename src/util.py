'''
Created on 2013.12.11.

@author: 502108836
'''
def striplist(L):
    return map(lambda l: l.strip(), L)

'''
    Returns the lines in the given file stripped from whitespaces.
    If omitEmpty, lines containing whitespaces only are omitted.
    Propagates read errors.
'''
def linesOfFile(path, omitEmpty=True):
    with  open(path) as f:
        lines=  striplist(f.readlines())
    if omitEmpty:
        lines= filter(lambda x: len(x) > 0, lines)
    return lines
    
    