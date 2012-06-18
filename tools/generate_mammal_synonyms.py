# generate list of mammal synonyms from Planet Mammiferes
import urllib2
from pyquery import PyQuery as p

URL = "http://www.planet-mammiferes.org/drupal/en/node/37?taxon=1"
response = urllib2.urlopen(URL).read()

results = p(response)('div#main div.content').__html__.split('<br>')
