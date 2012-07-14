import sys
from entered_data import *
import getpass
from get_mendeley_data import get_source_data

if len(sys.argv) > 1: email = sys.argv[1]
else: email = raw_input('mendeley email: ')
if len(sys.argv) > 2: password = sys.argv[2]
else: password = getpass.getpass('mendeley password: ')


def main():
    for taxon in species_list_data.keys():
        # generate species lists
        new_file = open('species_lists.%s.csv' % taxon, 'w')
        new_file.write('\n'.join(','.join(str(cell) for cell in line) for line in species_list_data[taxon]))
        new_file.close()

        # generate complete taxonomy
        tax_done = set()
        tax_file = open('taxonomy.%s.csv' % taxon, 'w')
        tax_file.write('taxon_id,spp_id,resource_id,scientific_name,genus,subgenus,species,subspecies,authority_name,authority_year,itis_number,common_name')
        for _, _, spp_id, _, _ in species_list_data[taxon][1:]:
            if not spp_id in tax_done:
                try:
                    tax_done.add(spp_id)
                    tax_file.write('\n' + ','.join(taxonomy_info[spp_id]))
                except KeyError: pass
        tax_file.close()

    source_file = open('sources.sources.csv', 'w')
    source_file.write('source_id,info_type,file_type,notes,isbn,author,title,journal,volume,issue,pages,year,url,tags')
    for source_url in sources:
        print source_url
        source_data = get_source_data(source_url, email, password)
        source_file.write('\n%s' % source_data)
    source_file.close()


if __name__ == '__main__':
    main()