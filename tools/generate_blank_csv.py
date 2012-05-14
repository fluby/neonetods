import os
import re

all_sql_files = [f for f in os.listdir('../') if f[-4:] == '.sql']

for data_file in all_sql_files:
    text = open('../' + data_file, 'r').read().replace('\n', '')
    create_table_statements = re.findall("CREATE [^;]*;", text)
    for table in create_table_statements:
        table_name, fields = table.split('(')[0], '('.join(table.split('(')[1:])
        table_name = table_name.lstrip('CREATE TABLE ')
        fields = [f.split()[0] for f in fields.rstrip(');').split(',')]
        output = open(table_name.replace('.', '_') + '_blank.csv', 'w')
        output.write(','.join(fields))
        output.close()