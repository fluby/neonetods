"""Restructure the NEON ETODS status table to include spp_id"""

#TODO
#No herps because I don't have the raw data
import csv
import numpy as np
import numpy.lib.recfunctions as nprf

from tax_resolve import tax_resolve

def get_csv_file(filename):
    """Import CSV data"""
    datafile = open(filename, 'r')
    datareader = csv.reader(datafile)
    data = []
    for row in datareader:
        if row[0]:
            data.append(row)
    return data

def export_to_csv(data, filename):
    """Export list of lists to comma delimited text file"""
    outputfile = open(filename, 'w')
    datawriter = csv.writer(outputfile)
    datawriter.writerows(data)
    outputfile.close()

def import_taxonomy_files(taxonomy_files, datadir):
    """Import the existing taxonomy files and store them in a single table"""
    taxon_dict = dict()
    for taxon in taxonomy_files:
        data = np.genfromtxt(datadir + taxon, delimiter=',', dtype=None, names=True)
        for name, spp_id in data[['scientific_name', 'spp_id']]:
            taxon_dict[name] = spp_id
    return taxon_dict

def remove_spaces(table):
    """Get rid of extra spaces from values in list of lists table"""
    cleaned_table = []
    for line in table:
        cleaned_line = []
        for item in line:
            cleaned_line.append(item.strip())
        cleaned_table.append(cleaned_line)
    return cleaned_table

def get_genus_sp_subsp(name):
    """Splits a scientific name into it's component part. Empty sting if no subsp"""
    names = name.split()
    if len(names) == 3:
        return names
    else:
        return names + ['']

def get_data_from_row(row):
    genus, sp, subsp, state, fed_status, state_status, notes, source = row 
    name = tax_resolve(genus, sp, subsp)
    spp_id = spp_ids.get(name, None)
    if fed_status:
        data_row = [fed_status, state_status, notes, '', 'http://www.mendeley.com/c/5405261894/g/2058663/listings-and-occurrences-for-each-state/', '']
    elif state_status: 
        data_row = [fed_status, state_status, '', notes, '', source]
    else:
        data_row = [fed_status, '', '', notes, '', source]
    return spp_id, state, data_row
    
datadir = '../data/'
taxonomy_files = ['beetles_clean.csv', 'ebird_tax_clean.csv', 'mammals.csv',
                  'mosquitoes.csv', 'plants.csv']

status_table = get_csv_file(datadir + 'status.csv') #using csv due to commas in comment fields
status_table = remove_spaces(status_table[:])
header_notentered = status_table[0]
del(status_table[0])
spp_ids = import_taxonomy_files(taxonomy_files, datadir)
status_table_dict = {}
sub_dict_fields = ['fed_status', 'state_status', 'fed_notes', 'state_notes',
                   'fed_source', 'state_source']
status_table_notadded = []
for row in status_table:
    spp_id, state, data_row = get_data_from_row(row)
    if spp_id:
        if (spp_id, state) in status_table_dict:
            current_data_row = status_table_dict[(spp_id, state)]
            for i, value in enumerate(current_data_row):
                if not value:
                    current_data_row[i] = data_row[i]
            data_row = current_data_row
        status_table_dict[(spp_id, state)] = data_row
    else:
        status_table_notadded.append(row)

status_table_clean = []
for key in status_table_dict:
    spp_id, state = key
    fed_status, state_status, fed_notes, state_notes, fed_source, state_source = status_table_dict[key]
    status_table_clean.append([spp_id, state, fed_status, state_status,
                               fed_notes, state_notes, fed_source, state_source])
    
status_table_notadded.insert(0, header_notentered)
export_to_csv(status_table_notadded, '../data/status_notentered.csv')
status_table_clean.insert(0, ['spp_id', 'state', 'fed_status', 'state_status',
                              'fed_notes', 'state_notes', 'fed_source', 'state_source'])
export_to_csv(status_table_clean, '../data/status_clean.csv')