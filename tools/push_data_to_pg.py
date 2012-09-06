import psycopg2 as dbapi
from getpass import getpass
from StringIO import StringIO
import sys
reload(sys)
sys.setdefaultencoding('latin-1')

def main():
    args = sys.argv[1:]
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

    connection = dbapi.connect(host=host, port=5432, user=user, password=password, database=database)
    cursor = connection.cursor()

    connection.set_client_encoding('latin-1')

    tables = [
            ('site_data.site_info_v11', ['../data/site_data_v11.csv']),
            ('sources.sources', ['sources.sources.csv']),
            ('taxonomy.high_level', ['../data/high_level.csv']),
            ('taxonomy.mammals', ['taxonomy.mammals.csv']),
            ('taxonomy.birds', ['taxonomy.birds.csv']),
            ('taxonomy.inverts', ['taxonomy.inverts.csv']),
            ('species_lists.species_lists', [
                                            'species_lists.mammals.csv',
                                            'species_lists.birds.csv',
                                            'species_lists.inverts.csv',
                                            ]),
            ('species_lists.status', ['../data/status.csv']),
            ]
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
            cursor.copy_expert(stmt, input_file)
            connection.commit()
            input_file.close()
        
        
    print 'done'
    connection.close()


if __name__ == '__main__':
    main()
