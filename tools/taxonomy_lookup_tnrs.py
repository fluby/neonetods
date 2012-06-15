import urllib2

URL = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names=%s"

def tnrs_lookup(name):    
    true, false, null = True, False, None
    name = name.replace(' ', '%20')
    response = urllib2.urlopen(URL % name).read()

    try:
        response_dict = eval(response)
        sci_name = response_dict['items'][0]['nameScientific']

        if sci_name: return sci_name
        return None
    except Exception as e:
        print e
        return None