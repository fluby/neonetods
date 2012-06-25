import urllib2
try:
    from tnrs_cache import tnrs_cache
except:
    tnrs_cache = {}

URL = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names=%s"

def tnrs_lookup(name):
    # lookup canonical plant names on TNRS web service
    true, false, null = True, False, None
    response = urllib2.urlopen(URL % name.replace(' ', '%20').read()

    try:
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
        open('tnrs_cache.py', 'w').write('tnrs_cache = %s' % tnrs_cache)
    return result