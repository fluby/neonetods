import difflib
from taxonomy_lookup_tnrs import tnrs_lookup
from taxonomy_lookup_itis import itis_lookup


# generate new spp_id when scientific name is not present in taxonomy tables
def spuh_1(genus):
    return '%s.sp' % genus[:3].lower()
def spuh_2(genus):
    return '%s_spp' % genus[:3].lower()
def slash_1(genus, all_species):
    return '%s%s' % (genus[:2].upper(), ''.join([sp[:2].upper() for sp in all_species]))
def slash_2(genus, all_species):
    return '%s_%s' % (genus[:3].upper(), '_'.join([sp[0].upper() for sp in all_species]))
spp_id_formats =    {
                    'mammals': (lambda genus, species: '%s_%s' % (genus[:3].lower(), species[:3].lower())),
                    'plants': (lambda genus, species: '%s_%s' % (genus[:3].lower(), species[:3].lower())),
                    'inverts': (lambda genus, species: '%s%s%s' % (genus[:2].lower(), species[:2].lower())),
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
ALL_SPP_IDS = dict()
def new_spp_id(taxon, genus, species=None, subspecies=None):
    try:
        all_species = None
        if species:
            for delimiter in (' x ', ' X ', '/'):
                if delimiter in species:
                    all_species = species.split(delimiter)
        name = (genus, species, subspecies)
        if name in ALL_SPP_IDS:
            return ALL_SPP_IDS[name]
        if genus and not species:
            result = spuh_formats[taxon](genus)
        elif species and all_species:
            result = slash_formats[taxon](genus, all_species)
        else:
            result = spp_id_formats[taxon](genus, species)
        n = 2
        orig_result = result
        while result in ALL_SPP_IDS.values():
            result = orig_result + str(n)
            n += 1
        ALL_SPP_IDS[name] = result
        return result
    except KeyError: return False
        


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

def tax_resolve_fuzzy(sci_name, synonyms=None, known_species=None, fuzzy=True, sensitivity=0.9):    
    """Performs fuzzy matching on a species name to determine whether it is in a list of synonyms or known species."""
    try: return synonyms[sci_name]
    except:
        if not fuzzy: return sci_name
        if not known_species: known_species = []
        if not synonyms: synonyms = {}
        all_taxes = synonyms.keys() + synonyms.values() + known_species
        scores = sorted([(key, difflib.SequenceMatcher(None, sci_name.lower(), key.lower()).ratio()) for key in all_taxes],
                         key=lambda s: s[1], reverse=True)
        top_score = scores[0]
        if top_score[1] >= sensitivity: return synonyms[top_score[0]] if top_score[0] in synonyms.keys() else top_score[0]
        else: return sci_name


syns = {
        'mammals': get_synonyms('../data/mammal_synonyms.csv'),
        'inverts': get_synonyms('../data/mosquito_synonyms.csv'),
        }

extra_steps = {
               'mammals': [lambda n: tax_resolve_fuzzy(n, synonyms=syns['mammals'])],
               'inverts': [lambda n: tax_resolve_fuzzy(n, synonyms=syns['inverts'])],
               'plants': [tnrs_lookup],
               }

def scientific_name(*args):
    return ' '.join([s for s in args if s])
def tax_resolve(genus, species, subspecies, com_name=None, taxon=None, known_species=None):
    if not known_species: known_species = []
    sci_name = scientific_name(genus, species, subspecies)
    
    name = sci_name
    if sci_name:
        new_name = tax_resolve_fuzzy(sci_name=sci_name, known_species=known_species)
        if new_name: name = new_name
    elif com_name:
        try:
            t = itis_lookup(com_name)
            if t: name = t
        except Exception as e:
            print '(%s)' % e,
    else: raise Exception("tax_resolve reqiures either scientific or common name")

    if name and taxon and taxon in extra_steps:
        steps = extra_steps[taxon]
        for step in steps:
            name = step(name)
    
    return name