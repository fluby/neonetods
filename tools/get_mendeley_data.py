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
    
    
def get_source_data(url):
    ''' resource_id  varchar(255)    NOT NULL,
        info_type    varchar(255),
        file_type    varchar(255),
        notes        text,
        isbn         varchar(255),
        author       varchar(255),
        title        varchar(255),
        journal      varchar(255),
        volume       integer,
        issue        integer,
        pages        varchar(255),
        year         integer,
        url          varchar(255),
        tags         varchar(255)'''
    data_doc = get_mendeley_data(url)
    
    source_data = []
    for key in ('', 'type', '', '', 'isbn', '', 'title', 'journal', 
                'volume', 'issue', 'pages', 'year', 'website', ''):
        try: source_data.append(str(data_doc[key]).replace('\\', ''))
        except KeyError: source_data.append('')
        
    try: source_data[5] = author_name(data_doc['author'])
    except: pass
    
    return source_data


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
