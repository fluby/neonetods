import sys
import os
import urllib
import urllib2
import re
from pyquery import PyQuery as p
import cPickle as pickle

from config import DATA_DIR

try: itis_cache = pickle.load(open(os.path.join(DATA_DIR, 'itis.cache'), 'r'))
except: itis_cache = {}

TIMEOUTS = 0


def itis_lookup(name, TIMEOUT=10):
    global TIMEOUTS

    name = name.replace("'", '').lower()
    if name in itis_cache:
        print "==> itis",
        return itis_cache[name]
    elif TIMEOUTS >= 5:
        # if ITIS seems to be down, do nothing
        raise Exception('ITIS seems to be down.')

    url = 'http://www.itis.gov/servlet/SingleRpt/SingleRpt'
    values = {'search_topic': 'all', 
              'search_kingdom':'every', 
              'search_span':'containing', 
              'search_value': name.decode(), 
              'categories':'All', 
              'source':'html', 
              'search_credRating': 'All'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req, timeout=TIMEOUT)
    html = response.read()
    response.close()

    # parse results to pull out unique species
    results = [s.tail for s in p(html)('td.body a')]
    results = sum([re.findall('Species: [A-Z][a-z ]*', result) for result in results], [])
    results = [s.split(':')[1].strip() for s in results]
    
    if results:
        genus = set()
        all_species = []
        for this_species in results:
            genus.add(this_species.split()[0])
            if len(genus) > 1: return False
            all_species.append(' '.join(this_species.split()[1:]))
        species = list(genus)[0] + ' ' + '/'.join(sorted(list(set(all_species))))
        itis_cache[name] = species
        print "==> itis",
    else:
        itis_cache[name] = False

    #print 'itis_cache = %s' % itis_cache
    pickle.dump(itis_cache, open(os.path.join(DATA_DIR, 'itis.cache'), 'w'), protocol=-1)

    return itis_cache[name]

if __name__=='__main__':
    name = raw_input('species name: ')
    print itis_lookup(name)
