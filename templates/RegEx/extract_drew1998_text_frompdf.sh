#!/bin/bash
# This script extracts the raw species data from the Drew_1998.pdf into a text file
pdftotext -f 9 -l 23 -x 0 -y 0 -W 250 -H 1000 -layout -nopgbrk Drew_1998.pdf drew_1998_left_column.txt
pdftotext -f 9 -l 23 -x 250 -y 0 -W 250 -H 1000 -layout -nopgbrk Drew_1998.pdf drew_1998_right_column.txt
cat drew_1998_left_column.txt drew_1998_right_column.txt > drew_1998_raw.txt
