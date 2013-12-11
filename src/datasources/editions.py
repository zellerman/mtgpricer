'''
Created on 2013.12.11.

@author: 502108836
'''

'''
No more chicken for the faint hearted, bitch!
'''

from util import striplist, linesOfFile
import logging
logger = logging.getLogger(__name__)

class EditionHandler(object):

    def __init__(self, path):
        self.edmap={}
        self.parseEditions(path)
    
    def parseEditions(self, path):
        entries= linesOfFile(path)
        for entry in entries:
            potofgold = entry.index('#')
            realname = entry[0:potofgold] 
            abbrs = striplist(entry[potofgold+1].split(','))
            for abbr in abbrs:
                if abbr in self.edmap:
                    logger.warn('%s is already mapped on %s therefore omitted to map %s', abbr, self.edmap[abbr], realname)
                else:
                    self.edmap[abbr]=realname
                    

    def __getitem__(self, key):
        if key not in self.edmap:
            logger.warn('No edition for abbreviation %s', key)
        return self.edmap.get(key, None)

        