import re
from datasources import database
from datasources.entities import Edition, EditionSexp
from util import linesOfFile

__author__ = '502108836'


def extractNames():
    lines = linesOfFile('tcgsetnames')
    names = []
    print len(lines)
    for line in lines:
        sn = re.search('">(.*?)</a>', line)
        if sn:
            print sn.group(1)
            names.append(sn.group(1))
        # else:
        #     print line
    print len(names)


def insertIdnSexps(idnset, src):
    # database.db = database.DB('../../res/expdb.db')
    for ed in idnset:
        edent = database.db.session.query(Edition).filter(Edition.name == ed).first()
        if edent:
            print edent
            edent.sexps.append(EditionSexp(ed, src))


def insertSexps(inp):
    database.db = database.DB('../../res/expdb.db')
    elems = linesOfFile(inp)
    eds = [e.split(',') for e in elems]
    for ed in eds:
        print ed
        edent = database.db.session.query(Edition).filter(Edition.name == ed[1]).first()
        if edent:
            print edent
            edent.sexps.append(EditionSexp(ed[0], 'http://magic.tcgplayer.com/db/price_guide.asp'))
    database.db.session.commit()
    # print eds


def gatsu():
    database.db = database.DB('../../res/expdb.db')
    dbnames = set(map(lambda e: e.name, database.db.session.query(Edition).order_by(Edition.name).all()))
    tcgnames = set(sorted(linesOfFile('tcgnames')))
    print sorted(tcgnames)
    print sorted(dbnames)
    inter = dbnames.intersection(tcgnames)
    print len(inter)
    print 'intersection', sorted(inter)
    tcgpos = sorted(tcgnames - dbnames)
    # print 'tcg-mci', tcgpos
    mcipos = sorted(dbnames - tcgnames)
    # print 'mci-tcg', mcipos
    for e in tcgpos:
        print e
    print 'faszo'
    for e in mcipos:
        print e

if __name__ == '__main__':
    # insertSexps('pukkancs')
    database.db = database.DB('../../res/expdb.db')
    dbnames = set(map(lambda e: e.name, database.db.session.query(Edition).order_by(Edition.name).all()))
    tcgnames = set(sorted(linesOfFile('tcgnames')))
    print sorted(tcgnames)
    print sorted(dbnames)
    inter = dbnames.intersection(tcgnames)
    print len(inter)
    print 'intersection', sorted(inter)

    insertIdnSexps(inter, 'http://magic.tcgplayer.com/db/price_guide.asp')
    database.db.session.commit()
