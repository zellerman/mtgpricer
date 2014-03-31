'''
Created on Mar 15, 2013

@author: davidborsodi
'''


def calc_price(usd):
    if usd < 0.26:
        return 50
    elif usd < 0.51:
        return 100
    elif usd < 1.00:
        return 200
    else:
        return int(round(usd * 200, -1))


def min_avg_mean(min, avg):
    return (min + avg) / 2 * 225


fifty = []
hun = []
twohun = []
over = []


def insert(cd, pr):
    if pr == 50:
        fifty.append((cd, str(pr)))
    elif pr == 100:
        hun.append((cd, str(pr)))
    elif pr == 200:
        twohun.append((cd, str(pr)))
    else:
        over.append((cd, str(pr)))


def ptlist(l):
    for e in l:
        print ' '.join(e)


def crappricer():
    cds = open('./crapp').readlines()

    total = 0
    for cd in cds:
        pr = cd.split()[-1]
        bu = cd.split()[0:-3]
        total += calc_price(float(pr))
        insert(' '.join(bu), calc_price(float(pr)))
    print '50/db'
    ptlist(fifty)
    print '\n'
    print '100/db'
    ptlist(hun)
    print '\n'
    print '200/db'
    ptlist(twohun)
    print '\n'
    print '200+'
    ptlist(over)
    print 'EV: ', total


def meanpricer(path):
    cds = open(path).readlines()

    total = 0
    for cd in cds:
        min = cd.split()[-1]
        avg = cd.split()[-2]
        bu = cd.split()[0:-3]
        shog = min_avg_mean(float(min), float(avg))
        print ' '.join(bu), shog
        total += shog
    print total


meanpricer('./krezganak')


    