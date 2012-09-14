import os
import sys
import getpass
from get_mendeley_data import get_source_data

from config import DATA_DIR
import cPickle as pickle
(species_list_data, taxonomy_info, sources, unknowns) = pickle.load(open(os.path.join(DATA_DIR, 'entered_data.pkl'), 'r'))


def main(*args):
    if len(args) > 0: email = args[0]
    else: email = raw_input('mendeley email: ')
    if len(args) > 1: password = args[1]
    else: password = getpass.getpass('mendeley password: ')

    source_file = open(os.path.join(DATA_DIR, 'sources.sources.csv'), 'w')
    source_file.write('source_id,info_type,file_type,notes,isbn,author,title,journal,volume,issue,pages,year,url,tags,spat_scale,spat_extent')
    completed_sources = set()
    failed_sources = []
    for n, source_url in enumerate(sources):
        if (n+1 % 100) == 0: print '%s/%s' % (n+1, len(sources))
        if not source_url in completed_sources:
            try:
                source_data = get_source_data(source_url, email, password)
                source_file.write('\n%s' % source_data)
            except: failed_sources.append(source_url)
            completed_sources.add(source_url)
    source_file.close()

    print 'Failed sources:', failed_sources
    failed_sources_path = os.path.join(DATA_DIR, 'failed_sources')
    if not os.path.exists(failed_sources_path): open(failed_sources_path, 'w').close()
    failed_sources_file = open(failed_sources_path, 'a')
    failed_sources_file.write('\n' + '\n'.join(failed_sources))
    failed_sources_file.close()

    for taxon in species_list_data.keys():
        # generate species lists
        new_file = open(os.path.join(DATA_DIR, 'species_lists.%s.csv' % taxon), 'w')
        lines = []
        seen_lines = set()
        for line in species_list_data[taxon]:
            if not line in seen_lines:
                source = line[0]
                if not source in failed_sources:
                    lines.append(line)
                seen_lines.add(line)
        new_file.write('\n'.join(','.join(str(cell) for cell in line) for line in lines))
        new_file.close()

        # generate complete taxonomy
        tax_done = set()
        tax_file = open(os.path.join(DATA_DIR, 'taxonomy.%s.csv' % taxon), 'w')
        tax_file.write('taxon_id,spp_id,resource_id,scientific_name,genus,subgenus,species,subspecies,authority_name,authority_year,itis_number,common_name')
        for _, _, spp_id in species_list_data[taxon][1:]:
            if not spp_id in tax_done:
                try:
                    tax_done.add(spp_id)
                    tax_file.write('\n' + ','.join([('"%s"' % s if s else '')
                                                    for s in taxonomy_info[spp_id]]))
                except KeyError: pass
        tax_file.close()


if __name__ == '__main__':
    main()
