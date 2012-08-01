import sys
reload(sys)
sys.setdefaultencoding('latin1')
import spynner
import re
from pyquery import PyQuery as p
import cPickle as pickle
try:
    itis_cache = pickle.load(open('itis.cache', 'r'))
except:
    itis_cache = {}


ITIS_URL = 'http://www.itis.gov/'

browser = spynner.Browser()

def itis_lookup(name, TIMEOUT=30):
    name = name.replace("'", '').lower()
    if name in itis_cache:
        print "==> itis",
        return itis_cache[name]

    success = browser.load(ITIS_URL)
    if not success: raise Exception('ITIS failed to load.')

    # fill in search box and submit form
    browser.fill('input#search', name.decode())
    browser.runjs('doSubmit();')

    # wait for results to load
    waits = 0
    html = browser.html
    while not 'results of' in html.lower() and not 'no data found' in html.lower():
        browser.wait(1)
        html = browser.html
        waits += 1
        if waits >= TIMEOUT:
            raise Exception('ITIS lookup timed out')

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
    pickle.dump(itis_cache, open('itis.cache', 'w'))

    return itis_cache[name]

if __name__=='__main__':
    name = raw_input('species name: ')
    print itis_lookup(name)
