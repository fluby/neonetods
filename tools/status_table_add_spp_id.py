"""Restructure the NEON ETODS status table to include spp_id"""

#TODO
#Ebird is currently not handled due to different structure
#No herps because I don't have the raw data
import csv
import numpy as np
import numpy.lib.recfunctions as nprf

import itis

from tax_resolve import tax_resolve

def get_csv_file(filename):
    """Import CSV data"""
    datafile = open(filename, 'r')
    datareader = csv.reader(datafile)
    data = []
    for row in datareader:
        if row:
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
    #TODO Resolve taxonomy using tax_resolve, at the moment one subsp may
    #overwrite another
    taxon_dict = dict()
    for taxon in taxonomy_files:
        data = np.genfromtxt(datadir + taxon, delimiter=',', dtype=None, names=True)
        for name, spp_id in data[['scientific_name', 'spp_id']]:
            #name = tax_resolve(genus, species, subsp)
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

    
datadir = '../data/'
taxonomy_files = ['beetles_clean.csv', 'ebird_tax_clean.csv', 'mammals.csv',
                  'mosquitoes.csv', 'plants.csv']

status_table = get_csv_file(datadir + 'status.csv') #using csv due to commas in comment fields
status_table = remove_spaces(status_table[:])
header = status_table[0]
del(status_table[0])
spp_ids = import_taxonomy_files(taxonomy_files, datadir)
status_table_clean = []
status_table_notadded = []
for row in status_table:
    genus, sp, subsp, state, fed_status, st_status, notes, source = row
    name = tax_resolve(genus, sp, subsp)
    #TODO Actually change the species name and associated columns
    spp_id = spp_ids.get(name, None)
    if spp_id:
        new_row = [spp_id] + get_genus_sp_subsp(name) + row[3:]
        status_table_clean.append(new_row)
    else:
        status_table_notadded.append(row)
    
status_table_notadded.insert(0, header)
export_to_csv(status_table_notadded, '../data/status_notentered.csv')
header.insert(0, 'spp_id')
status_table_clean.insert(0, header)
export_to_csv(status_table_clean, '../data/status_clean.csv')