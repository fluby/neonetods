import os
import urllib2
from config import DATA_DIR
import cPickle as pickle
try: tnrs_cache = pickle.load(open(os.path.join(DATA_DIR, 'tnrs.cache'), 'r'))
except: tnrs_cache = {}

URL = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names=%s"
TIMEOUTS = 0


def tnrs_lookup(name, TIMEOUT=10):
    global TIMEOUTS
    try: return tnrs_cache[name]
    except:
        if TIMEOUTS >= 5:
            # if TNRS seems to be down, do nothing
            raise Exception('TNRS seems to be down.')

    # lookup canonical plant names on TNRS web service
    true, false, null = True, False, None
    try:
        response = urllib2.urlopen(URL % name.replace(' ', '%20'), timeout=TIMEOUT)
        html = response.read()

        response_dict = eval(html)
        sci_name = response_dict['items'][0]['nameScientific']

        if sci_name: result = sci_name
        else: result = None

	response.close()

    except urllib2.URLError:
        TIMEOUTS += 1

    except Exception as e:
        print e
        result = None

        try: response.close()
        except: pass

    # cache results and return
    if result:
        tnrs_cache[name] = result
        pickle.dump(tnrs_cache, open(os.path.join(DATA_DIR, 'tnrs.cache'), 'w'), protocol=-1)
    return result
