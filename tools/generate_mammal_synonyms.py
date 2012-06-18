# generate list of mammal synonyms from Planet Mammiferes
import urllib2
from pyquery import PyQuery as p
import re
import sys
reload(sys)
sys.setdefaultencoding('latin1')

URL = "http://www.planet-mammiferes.org/drupal/en/node/37?taxon=1"
response = urllib2.urlopen(URL).read()

results = p(response)('div#main div.content').__html__().split('<br>')
output_file = open('../data/mammal_synonyms.csv', 'w')
output_file.write('unaccepted_synonym,accepted_synonym')
for result in results:
    if '<strong>' in result and '=' in result:
        try:
            new_name = re.findall('\>.*\<', result)[0][1:-1]
            old_names = re.findall('=[^=]*=', result)
            for old_name in old_names:
                old_name = old_name.replace('=', '').strip()
                if old_name:
                    print new_name, old_name
                    output_file.write('\n%s,%s' % (old_name, new_name))
        except IndexError as e:
            print '****', result, e