"""Cleanup bad source URLS"""

import csv

import numpy as np

def get_csv_file(filename):
    """Import CSV data"""
    datafile = open(filename, 'r')
    datareader = csv.reader(datafile)
    data = []
    for row in datareader:
        if row[0]:
            data.append(row)
    return data

def write_csv_file(data, filename):
    """Export CSV data"""
    output_file = open(filename, 'w')
    datawriter = csv.writer(output_file)
    datawriter.writerows(data)
    output_file.close()    

def get_source_matching_dict(path):
    source_matching_table = get_csv_file(path)
    return dict(source_matching_table)
    
def clean_species_lists(taxa, source_matching_dict):
    """Clean species list files"""
    for taxon in taxa:
        data = get_csv_file('../data/sp_list_%s_raw.csv' % taxon)
        cleaned_data = []
        for line in data:
            if line[-1] in source_matching_dict.keys():
                line[-1] = source_matching_dict[line[-1]]
                print taxon, line[-1]
            cleaned_data.append(line)
        write_csv_file(cleaned_data, '../data/sp_list_%s.csv' % taxon)

def main():
    source_matching_table_path = '../data/failed_sources_corrected_urls.csv'
    source_matching_dict = get_source_matching_dict(source_matching_table_path)
    taxa = ['birds', 'herps', 'inverts', 'mammals', 'plants']
    clean_species_lists(taxa, source_matching_dict)
    
if __name__ == "__main__":
    main()