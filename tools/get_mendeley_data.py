import urllib2 as u
import pyquery as p
import mechanize
import getpass
import cPickle as pickle
import os

import dodobase.data as data
DATA_DIR = '/'.join(data.__file__.split('/')[:-1]) + '/'

try: mendeley_cache = pickle.load(open(os.path.join(DATA_DIR, 'mendeley.cache'), 'r')) 
except: mendeley_cache = {}
try: group_docs = pickle.load(open(os.path.join(DATA_DIR, 'group_docs.pkl'), 'r'))
except: from get_all_group_docs import all_docs as group_docs

b = mechanize.Browser()
b.set_handle_robots(False)


def get_mendeley_data(url, email=None, password=None):
    """Given a Mendeley article URL, returns a dictionary containing citation information."""
    if url[:4] == 'www.': url = 'http://' + url
    if url in mendeley_cache: return mendeley_cache[url]

    if url in group_docs: 
        data_doc = group_docs[url]
        data_doc['tags'] = ','.join(data_doc['tags'])
    else:
        b.open(url)
        new_url = b.response().geturl()
        if 'login' in new_url:
            b.select_form(nr=1)
            b['email'] = email
            b['password'] = password
            b.submit()
            new_url = b.response().geturl()
            if not new_url == url: raise('Failed to login.')

        if new_url in group_docs: 
            data_doc = group_docs[new_url]
            data_doc['tags'] = ','.join(data_doc['tags'])
        else:
            html = b.response().read()

            true, false = True, False

            data_doc = p.PyQuery(html)("article")[0].get("data-doc")

            if '&quot;' in data_doc: data_doc = data_doc.replace('&quot;', '"')
            if '\\' in data_doc: data_doc = data_doc.replace('\\', '')

            data_doc = eval(data_doc)
            tags = p.PyQuery(html)('div.tags-list')
            if tags:
                data_doc['tags'] = ','.join(a.text for a in tags.find('a'))
            else: data_doc['tags'] = ''
        

    if data_doc['title'][-1] == '.': data_doc['title'] = data_doc['title'][:-1]

    mendeley_cache[url] = data_doc
    pickle.dump(mendeley_cache, open(os.path.join(DATA_DIR, 'mendeley.cache'), 'w'))
    
    return data_doc
    
    
def get_source_data(url, email=None, password=None):
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
    data_doc = get_mendeley_data(url, email, password)
    
    source_data = []
    for key in ('', 'type', '', '', 'isbn', '', 'title', 'journal', 
                'volume', 'issue', 'pages', 'year', 'website', 'tags', 
                'spat_scale', 'spat_extent'):
        try: source_data.append(str(data_doc[key]).replace('\\', ''))
        except KeyError: source_data.append('')
        
    source_data[0] = url
    try: source_data[5] = author_name(data_doc['author'])
    except: pass
    
    return ','.join(('"%s"' % source if source else '') for source in source_data)


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


if __name__ == '__main__':
    url = raw_input('url: ')
    email = raw_input('mendeley email: ')
    password = getpass.getpass('mendeley password: ')
    print get_mendeley_data(url, email, password)
