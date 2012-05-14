import urllib2 as u
import pyquery as p


def get_mendeley_data(url):
    """Given a Mendeley article URL, returns a dictionary containing citation information."""
    html = u.urlopen(url).read()

    true, false = True, False

    return eval(p.PyQuery(html)("article")[0].get("data-doc"))