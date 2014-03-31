import time

###
###time manipulation
###
import unicodedata

currentTimeMillis = lambda: int(round(time.time() * 1000))

dayToSec = lambda d: 24 * 60 * 60 * d

###
###string collection manipulation
###


def lowerize(L):
    return map(lambda l: l.lower(), L)


def striplist(L):
    return map(lambda l: l.strip(), L)


###
###fileutils
###

def linesOfFile(path, omitEmpty=True):
    """
        Returns the lines in the given file stripped from whitespaces.
        If omitEmpty, lines containing whitespaces only are omitted.
        Propagates read errors.
    """
    with  open(path) as f:
        lines = striplist(f.readlines())
    if omitEmpty:
        lines = filter(lambda x: len(x) > 0, lines)
    return lines


def strip_accents(s):
    print ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))