import difflib


# generate new spp_id when scientific name is not present in taxonomy tables
def spuh_1(genus):
    return '%s.sp' % genus[:3].upper()
def spuh_2(genus):
    return '%s_spp' % genus[:3].upper()
def slash_1(genus, sp1, sp2):
    return '%s%s%s' % (genus[:2].upper(), sp1[:2].upper(), sp2[:2].upper())
def slash_2(genus, sp1, sp2):
    return '%s_%s_%s' % (genus[:3].upper(), sp1[0].upper(), sp2[0].upper())
spp_id_formats =    {
                    'mammals': (lambda genus, species, n=None: '%s_%s' % (genus[:3], species[:3])),
                    'plants': (lambda genus, species, n=None: '%s_%s' % (genus[:3].upper(), species[:3].upper())),
                    'inverts': (lambda genus, species, n=None: '%s%s%s' % (genus[:2].upper(), species[:2].upper(), n if n else '')),
                    }
spuh_formats =      {
                    'mammals': spuh_2,
                    'plants': spuh_1,
                    'inverts': spuh_1,
                    }
slash_formats =     {
                    'mammals': slash_2,
                    'plants': slash_1,
                    'inverts': slash_1,
                    }
def new_spp_id(tax_group, genus, species, sp2=None):
    if genus and not species:
        return spuh_formats[tax_group](genus)
    elif species and sp2:
        return slash_formats[tax_group](genus, species, sp2)
    else:
        return spp_id_formats[tax_group](genus, species)


# check synonym list for known synonyms, and resolve small differences
def get_synonyms(input_files, wrong_col=0, right_col=1):
    """Get a dictionary of species name synonyms from an input file."""
    if isinstance(input_files, str):
        input_files = [input_files]
    syn = {}
    for input_file in input_files:
        data_file = open(input_file, 'r')
        data_file.readline()
        for line in data_file:
            cols = [s.strip() for s in line.split(',')]
            wrong_name = cols[wrong_col]
            right_name = cols[right_col]
            syn[wrong_name] = right_name
    return syn

    
def tax_resolve(sci_name=None, com_name=None, syns=None):
    if not syns: syns = {}
    
    if sci_name:
        name = sci_name
        t = tax_resolve_fuzzy(sci_name, syns)
        if t: name = t
    elif com_name:
        name = com_name
        t = tax_resolve_itis(com_name)
        if t: name = t
    else: raise Exception("tax_resolve reqiures either scientific or common name")
    
    return name
    

def tax_resolve_fuzzy(tax, synonyms, sensitivity=0.85):
    """Performs fuzzy matching on a species name to determine whether it is in a list of synonyms."""
    if (not synonyms) or tax in synonyms.values(): return tax
    all_taxes = synonyms.keys() + synonyms.values()
    scores = sorted([(key, difflib.SequenceMatcher(None, tax.lower(), key.lower()).ratio()) for key in all_taxes],
                    key=lambda s: s[1], reverse=True)
    top_score = scores[0]
    if top_score[1] >= sensitivity: return synonyms[top_score[0]] if top_score[0] in synonyms.keys() else top_score[0]
    return False
    
def tax_resolve_itis(common_name):
    """Query ITIS for a species name and return the accepted scientific name."""
    pass
