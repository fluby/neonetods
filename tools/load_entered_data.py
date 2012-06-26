import sys
reload(sys)
sys.setdefaultencoding('latin1')
import tax_resolve
from taxonomy_lookup_itis import itis_lookup


species_lists = [
                 ('mammals', '../data/sp_list_mammals.csv', [('../data/mammals.csv', 1, 3)]),
                 ('birds', '../data/sp_list_birds.csv',     [('../data/ebird_tax_clean.csv', 0, 1)]),
                 ('plants', '../data/sp_list_plants.csv',   [('../data/plants.csv', 2, 3)]),
                 ('inverts', '../data/sp_list_inverts.csv', [('../data/beetles.csv', 1, 3), 
                                                             ('../data/mosquitoes.csv', 1, 3)]),
                 #herps
                 ]


def get_spp_id(genus, species, subspecies, com_name, taxon, spp_code_dict):
    '''Get spp_id from spp_id dictionary. Returns: 
        a spp_id string if this is a known or unknown species,
        None if only an ambiguous common_name was given'''
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
            if new_name:
                try:
                    return spp_code_dict[new_name]
                except KeyError:
                    new_spp_id = tax_resolve.new_spp_id(taxon, *new_name.split())
                    if new_spp_id:
                        spp_code_dict[new_name] = new_spp_id
                        return new_spp_id
            return None
        
                 
                 
for taxon, data_entry_file, spp_code_files in species_lists:
    print '*** %s ***' % taxon
    spp_codes = {}
    for (spp_file, spcode_col, sciname_col) in spp_code_files:
        data_file = open(spp_file, 'r')
        data_file.readline()
        for line in data_file:
            line = line.strip()
            if line:
                cols = line.split(',')
                spp_code = cols[spcode_col]
                sci_name = cols[sciname_col]
                spp_codes[sci_name] = spp_code
                tax_resolve.ALL_SPP_IDS[sci_name] = spp_code
        data_file.close()
    correct = 0
    unknown = 0

    data_file = open(data_entry_file, 'r')
    data = data_file.read().replace('\r', '\n')
    lines = data.split('\n')[1:]
    for line in lines:
        line = line.strip()
        if line:
            try:
                site,genus,sp,subsp,common_name,source = [s.strip() for s in line.split(',')]
                print genus, sp, subsp, common_name,
                spp_id = get_spp_id(genus, sp, subsp, com_name=common_name,
                                    taxon=taxon, spp_code_dict=spp_codes)
                if spp_id: 
                    correct += 1
                    print '->', spp_id
                else:
                    unknown += 1
                    print '**UNKNOWN**'
            #except KeyboardInterrupt: raise
            except Exception as e: print line, e; unknown += 1
    print '%s: Correct: %s; Unknown: %s (%s)' % (taxon, correct, unknown, correct / float(correct + unknown))
