"""Extract Genus species from Drew_1998. We are looking to find 1013 entries."""

import re

inputfile = open('drew_1998_raw.txt')
outputdata=[]
subspdata=[]
altdata=[]

regex = "([A-Z][a-z]+)\s+([a-z][a-z]+\\-?[a-z]+) " #1002 entries
regexsub = "(var.|x|subsp.)\s([a-z]+)"

for line in inputfile:
    match = re.search(regex, line)
    submatch = re.search(regexsub, line)
    if match:
        output = match.group(1) + ',' + match.group(2) + ','
        if submatch:
            output += submatch.group(2)
        output += '\n'
        outputdata.append(output)

textfile = open('Drew1998_output.csv','w')
textfile.writelines(outputdata)
textfile.close()            