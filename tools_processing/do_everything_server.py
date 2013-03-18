import os
import cPickle as pickle
from config import DATA_DIR

def do_everything(species_lists):
    import load_entered_data as m1
    if not species_lists: species_lists = m1.default_species_lists
    correct, unknown = m1.main(species_lists)
    
    return correct, unknown
    
    
if __name__ == '__main__':
    do_everything(None)    