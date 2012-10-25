"""Restructure the NEON ETODS status table to include spp_id"""

#TODO
#Ebird is currently not handled due to different structure
#No herps because I don't have the raw data
import csv
import numpy as np
import numpy.lib.recfunctions as nprf

#from tax_resolve import tax_resolve

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
        
datadir = '../data/'
taxonomy_files = ['beetles_clean.csv', 'ebird_tax_clean.csv', 'mammals.csv',
                  'mosquitoes.csv', 'plants.csv']

status_table = get_csv_file(datadir + 'status.csv') #using csv due to commas in comment fields
status_table = remove_spaces(status_table[:])
spp_ids = import_taxonomy_files(taxonomy_files, datadir)
status_table_restructured = []
for row in status_table:
    name = ' '.join(row[0:2]) #why there are spaces after the csv import I do not know
    new_row = [spp_ids.get(name, 'unknown')] + row
    status_table_restructured.append(new_row)
status_table_restructured[0][0] = 'spp_id'
export_to_csv(status_table_restructured, '../data/status_spp_id.csv')