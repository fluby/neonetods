# usage: python do_everything.py [postgres username] [postgres password]
import sys

import load_entered_data as m1
m1.main(m1.default_species_lists)
import output_csvs as m2
m2.main()
import pg_interface as m3
m3.get_connection(sys.argv[1:])
m3.push_data()