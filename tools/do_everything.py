# usage: python do_everything.py [postgres username] [postgres password]
import sys

user = None
password = None
if len(sys.argv) > 1: user = sys.argv[1]
if len(sys.argv) > 2: password = sys.artv[2]

import load_entered_data as m1
m1.main()
import output_csvs as m2
m2.main()
import load_to_db as m3
m3.main(user, password)