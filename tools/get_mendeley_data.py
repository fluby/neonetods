import urllib2 as u
import pyquery as p


def get_mendeley_data(url):
    """Given a Mendeley article URL, returns a dictionary containing citation information."""
    if url[:4] == 'www.': url = 'http://' + url
    html = u.urlopen(url).read()

    true, false = True, False

    data_doc = eval(p.PyQuery(html)("article")[0].get("data-doc"))
    if data_doc['title'][-1] == '.': data_doc['title'] = data_doc['title'][:-1]
    
    return data_doc


def author_name(author):
    """Returns an author name (last, first) from a Mendeley author name dictionary."""
    surname, forename = author['surname'], author['forename']
    forename = ' '.join([n[0] + '.' for n in forename.split(' ')])

    return ', '.join((surname, forename))

def author_string(authors):
    """Given a list of authors, returns a string containing all of the authors."""
    if len(authors) > 1:
        authors[-1]['surname'] = '& ' + authors[-1]['surname']
    return ', '.join([author_name(author) for author in authors])


def citation(data_doc):
    """Returns a citation string from a Mendeley data-doc dictionary."""
    if isinstance(data_doc, str):
        data_doc = get_mendeley_data(data_doc)

    citation = "%s %s. %s %s, %s (%s)." % (author_string(data_doc['authors']), 
                                           data_doc['title'], 
                                           data_doc['published_in'], data_doc['volume'], data_doc['pages'], data_doc['year'])
    return citation