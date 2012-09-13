from config import DATA_DIR, groups
import psycopg2 as dbapi
from getpass import getpass
from StringIO import StringIO
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('latin-1')


connection = None

def get_connection(*args):
    if args: user = args[0]
    else: user = raw_input('postgres username: ')
    if len(args) > 1: password = args[1]
    else: password = getpass('postgres password:')
    if len(args) > 2: host = args[2]
    else: 
        host = raw_input('host: ')
        if not host: 'serenity.bluezone.usu.edu'
    if len(args) > 3: database = args[3]
    else:
        database = raw_input('database: ') 
        if not database: database = 'dodobase'
    
    global connection
    connection = dbapi.connect(host=host, port=5432, user=user, password=password, database=database)
    
    connection.set_client_encoding('latin-1')



def create_databases():
    global connection
    if connection is None: get_connection()
    cursor = connection.cursor()

    sql_files = [f for f in os.listdir('..') if f.endswith('.sql')]
    failures = True
    tries = 0
    while failures:
        tries += 1
        failures = []
        for sql_file in sql_files:
            print sql_file
            contents = open('../%s' % sql_file).read()
            try:
                try:
                    cursor.execute(contents)
                except:
                    contents = contents[2:]
                    cursor.execute(contents)
            except dbapi.ProgrammingError as e:
                print e
                connection.rollback()
                failures.append(sql_file)
        if failures:
            if tries > sum(range(len(sql_files)+1)): 
                sql_files = failures


def push_data(tables=None):
    global connection
    if connection is None: get_connection()
    cursor = connection.cursor()

    if tables is None:
        tables = ([
            ('site_data.site_info', [os.path.join(DATA_DIR, 'site_data_v11.csv')]),
            ('sources.sources', [os.path.join(DATA_DIR, 'sources.sources.csv')]),
            ('taxonomy.high_level', [os.path.join(DATA_DIR, '../data/high_level.csv')]),
            ] 
            + [('taxonomy.%s' % group, [os.path.join(DATA_DIR, 'taxonomy.%s.csv' % group)]) for group in groups]
            + [('species_lists.%s' % group, [os.path.join(DATA_DIR, 'species_lists.%s.csv' % group)]) for group in groups]
            #+ [('species_lists.status', ['../data/status.csv']),]
            )
            
    for table, files in tables:
        try:
            cursor.execute('DELETE FROM %s;' % table)
        except:
            connection.rollback()
    
        for file in files:
            input_file = open(file, 'r')
            #input_file.readline()
            print table, file
            stmt = "COPY %s FROM stdin WITH DELIMITER ',' NULL AS '' CSV HEADER;" % (table)
            try:
                cursor.copy_expert(stmt, input_file)
                connection.commit()
            except Exception as e:
                print 'EXCEPTION:', e
                connection.rollback()
            input_file.close()
            

    # de-duplicate species lists
    for group in groups:
        cursor.execute('''DELETE FROM species_lists.%s
                      WHERE source_id NOT IN (SELECT min(source_id)
                      FROM species_lists.%s
                      GROUP BY source_id, site_id, spp_id)''' % (group, group))
        
        
    print 'done'
    connection.close()


def get_species_list(taxon, site):
    global connection
    if connection is None: get_connection()
    cursor = connection.cursor()

    table = 'species_lists.species_lists'
    stmt = 'SELECT DISTINCT spp_id FROM %s' % table


if __name__ == '__main__':
    create_databases()
    push_data()
