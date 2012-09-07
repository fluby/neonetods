import sys
reload(sys)
sys.setdefaultencoding('latin1')
import csv
import tax_resolve
import getpass
import cPickle as pickle
from taxonomy_lookup_itis import itis_lookup


default_synonyms = {
                    'mammals': [('../data/mammals.csv', 1, [(3, False), (11, True)])],
                    'birds': [('../data/ebird_tax_clean.csv', 0, [(1,False),(2,True)])],
                    'plants': [('../data/plants.csv', 2, 3)],
                    'inverts': [('../data/beetles.csv', 1, 3), 
                                ('../data/mosquitoes.csv', 1, 3)],
                    #herps
                    }

default_species_lists = [
                         ('mammals', '../data/sp_list_mammals.csv'),
                         ('birds', '../data/sp_list_birds.csv'),
                         ('plants', '../data/sp_list_plants.csv'),
                         ('inverts', '../data/sp_list_inverts.csv'),
                         ]

def col_split(line):
    return csv.reader([line], dialect=csv.excel, delimiter=',').next()

def format_line(line):
    return line.strip().replace('\xef\xbf\xbd', "'")
    
def get_spp_id(genus, species, subspecies, com_name, taxon, spp_code_dict):
    '''Get spp_id from spp_id dictionary. Returns: 
        a spp_id string if this is a known or unknown species,
        None if only an ambiguous common_name was given'''
    try:
        result = spp_code_dict[com_name.lower()]
        return result
    except KeyError: pass
    sci_name = tax_resolve.scientific_name(genus, species, subspecies)
    try:
        # return species id for species, if we have one
        return spp_code_dict[sci_name]
    except KeyError:
        for delimiter in (' x ', ' X ', '/'):
            # hybrids and slashes
            if len(species.split(delimiter)) > 1:
                children = species.split(delimiter)
                if all([get_spp_id(child) for child in children]):
                    # create a new species id for the hybrid/slash
                    new_spp_id = tax_resolve.new_spp_id(taxon, genus, species, subspecies)
                else:
                    # we don't have a species code for all of the species in the hybrid/slash
                    return None
        else:
            new_name = tax_resolve.tax_resolve(genus, species, subspecies, com_name=com_name, known_species=spp_code_dict.keys(), taxon=taxon)
            if new_name != sci_name:
                print '==> corrected to %s' % new_name,
                sys.stdout.flush()
            if new_name:
                try:
                    return spp_code_dict[new_name]
                except KeyError:
                    corrected_sci_name = (new_name.split('(')[0].strip()).split()
                    new_spp_id = tax_resolve.new_spp_id(taxon, *corrected_sci_name)
                    if new_spp_id:
                        spp_code_dict[new_name] = new_spp_id
                        pickle.dump(spp_code_dict, open('%s.spp_codes.cache' % taxon, 'w'), protocol=-1)
                        return new_spp_id
            return None
        
                 
                 
def main(species_lists):
    species_list_data = {}
    taxonomy_info = {}
    sources = []
    unknowns = []

    species_lists = [(tax, file,) + (default_synonyms[tax],) for tax, file in species_lists]
    for tax, _, _ in species_lists:
        species_list_data[tax] = [('source_id','site_id','spp_id')]

    # run through all entered data, generate a species id, and output 
    # species lists and taxonomies into CSV files
    for taxon, data_entry_file, spp_code_files in species_lists:
        print '*** %s ***' % taxon
        try:
            spp_codes = pickle.load(open('%s.spp_codes.cache' % taxon, 'r'))
        except:
            spp_codes = {}
        
            # read known species ids
            for (spp_file, spcode_col, sciname_col) in spp_code_files:
                data_file = open(spp_file, 'r')
                data_file.readline()
                for line in data_file:
                    line = format_line(line)
                    cols = col_split(line)
                    if line:
                        spp_code = cols[spcode_col]
                        if isinstance(sciname_col, list):
                            name_cols = sciname_col
                        else:
                            name_cols = [(sciname_col, False)]
                        for name_col, common in name_cols:
                            name = cols[name_col]
                            if name:
                                if common: name = name.lower()
                                spp_codes[name] = spp_code
                                tax_resolve.ALL_SPP_IDS[name] = spp_code
                data_file.close()
            
            pickle.dump(spp_codes, open('%s.spp_codes.cache' % taxon, 'w'), protocol=-1)
        correct = 0
        unknown = 0

        # parse entered data
        data_file = open(data_entry_file, 'r')
        data = data_file.read().replace('\r', '\n')
        lines = data.split('\n')[1:]
        for line in lines:
            line = format_line(line)
            if line:
                try:
                    site,genus,sp,subsp,common_name,source = [s.strip() for s in col_split(line)]
                    print genus, sp, subsp, common_name,
                    sys.stdout.flush()
                    spp_id = get_spp_id(genus, sp, subsp, com_name=common_name,
                                        taxon=taxon, spp_code_dict=spp_codes)
                    if spp_id: 
                        correct += 1
                        print '->', spp_id
                        sources.append(source)
                        species_list_data[taxon].append((source, site, spp_id))
                        sci_name = ' '.join([n for n in (genus, sp, subsp) if n])
                        taxonomy_info[spp_id] = (taxon, spp_id, '', sci_name, genus, '', sp, subsp, '', '', '', common_name)
                    else:
                        unknown += 1
                        unknowns.append(line)
                        print '**UNKNOWN**'
                #except KeyboardInterrupt: raise
                except Exception as e: print line, e; unknown += 1
        print '%s: Correct: %s; Unknown: %s (%s)' % (taxon, correct, unknown, correct / float(correct + unknown))

    # output parsed data to separate file
    output_file = open('entered_data.py', 'w')
    data = '\n'.join(['%s = %s' % (var, locals()[var]) for var in ('species_list_data', 'taxonomy_info', 'sources', 'unknowns')])
    output_file.write(data)
    output_file.close()

        
if __name__ == '__main__':
    main(default_species_lists)
