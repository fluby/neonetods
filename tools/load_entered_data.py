import tax_resolve


species_lists = [
                 ('mammals', '../templates/sp_list_mammals.csv', [('../data/mammals.csv', 1, 3)], None),
                 #('birds', '../templates/sp_list_birds.csv',     [('../data/birds.csv', 0, 0)], None),
                 ('plants', '../templates/sp_list_plants.csv',   [('../data/plants.csv', 2, 3)], None),
                 ('inverts', '../templates/sp_list_inverts.csv', [('../data/beetles.csv', 1, 3), 
                                                                  ('../data/mosquitoes.csv', 1, 3)],
                                                                 ['../data/mosquito_synonyms.csv']),
                 #herps
                 ]


def get_spp_code(sci_name, spp_code_dict, tax_resolve):
    if sci_name in spp_code_dict:
        return spp_code_dict[sci_name]
    else:
        sci_name = tax_resolve[sci_name]
                 
                 
for taxon, data_entry_file, spp_code_files, synonyms_files in species_lists:
    print '*** %s ***' % taxon
    spp_codes = {}
    if synonyms_files:
        syns = tax_resolve.get_synonyms(synonyms_files)
    else: syns = {}
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
        data_file.close()
    data_file = open(data_entry_file, 'r')
    data = data_file.read().replace('\r', '\n')
    lines = data.split('\n')[1:]
    for line in lines:
        line = line.strip()
        if line:
            site,genus,sp,subsp,common_name,source = [s.strip() for s in line.split(',')]
            if genus and sp:
                sci_name = '%s %s' % (genus, sp)
                if sci_name in spp_codes:
                    print '%s: %s' % (sci_name, spp_codes[sci_name])
                else:
                    corrected_name = tax_resolve.tax_resolve(sci_name, com_name=common_name if common_name else None, 
                                                             syns=syns)
                    if corrected_name and corrected_name in spp_codes:
                        print 'corrected: %s: %s' % (sci_name, spp_codes[corrected_name])
                    else:
                        print '**%s' % sci_name
            elif common_name:
                corrected_name = tax_resolve.tax_resolve(com_name=common_name, syns=syns)
                print '**%s' % common_name
