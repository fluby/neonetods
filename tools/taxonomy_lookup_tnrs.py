import urllib2
import cPickle as pickle
try: tnrs_cache = pickle.load(open('tnrs.cache', 'r'))
except: tnrs_cache = {}

URL = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names=%s"

def tnrs_lookup(name, TIMEOUT=10):
    # lookup canonical plant names on TNRS web service
    true, false, null = True, False, None
    try:
        response = urllib2.urlopen(URL % name.replace(' ', '%20'), timeout=TIMEOUT).read()

        response_dict = eval(response)
        sci_name = response_dict['items'][0]['nameScientific']

        if sci_name: result = sci_name
        else: result = None

    except Exception as e:
        print e
        result = None

    # cache results and return
    if result:
        tnrs_cache[name] = result
        pickle.dump(tnrs_cache, open('tnrs.cache', 'w'), protocol=-1)
    return result