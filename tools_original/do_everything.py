# usage: python do_everything.py [postgres username] [postgres password]
import sys
import os
from config import DATA_DIR


def do_everything(species_lists, output_csvs_args, connection_args):
    import load_entered_data as m1
    if not species_lists: species_lists = m1.default_species_lists
    correct, unknown = m1.main(species_lists)
    import output_csvs as m2
    m2.main(*output_csvs_args)
    import pg_interface as m3
    m3.get_connection(*connection_args)
    groups = list(set(str(s[0]) for s in species_lists))
    m3.push_data(groups)
    
    return correct, unknown
    
if __name__ == '__main__':
    do_everything(None, sys.argv[1:3], sys.argv[3:])
