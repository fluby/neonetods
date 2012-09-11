import sys
from entered_data import *
import getpass
from get_mendeley_data import get_source_data

if len(sys.argv) > 1: email = sys.argv[1]
else: email = raw_input('mendeley email: ')
if len(sys.argv) > 2: password = sys.argv[2]
else: password = getpass.getpass('mendeley password: ')


def main():
    source_file = open('sources.sources.csv', 'w')
    source_file.write('source_id,info_type,file_type,notes,isbn,author,title,journal,volume,issue,pages,year,url,tags,spat_scale,spat_extent')
    completed_sources = set()
    failed_sources = []
    for n, source_url in enumerate(sources):
        print '%s/%s' % (n+1, len(sources))
        if not source_url in completed_sources:
            try:
                source_data = get_source_data(source_url, email, password)
                source_file.write('\n%s' % source_data)
            except: failed_sources.append(source_url)
            completed_sources.add(source_url)
    source_file.close()

    print 'Failed sources:', failed_sources


    for taxon in species_list_data.keys():
        # generate species lists
        new_file = open('species_lists.%s.csv' % taxon, 'w')
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
        tax_file = open('taxonomy.%s.csv' % taxon, 'w')
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
