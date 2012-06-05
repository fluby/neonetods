"""Extract Genus species from Drew_1998. We are looking to find 1013 entries."""

import re

inputfile = open('Drew_1998_splist.txt')
currentline = inputfile.readline()
outputdata=[]
subspdata=[]
altdata=[]

regex = ".([A-Z][a-z]+)\s+([a-z][a-z]+\\-?[a-z]+) " #1002 entries

regexalt = ( " ([A-Z][a-z]+).+([a-z]+) ",
            ".([A-Z][a-z]+) ([a-z]+)." #1030 entries
            )

regexsub = ".([A-Z][a-z]+)\s+([a-z][a-z]+\\-?[a-z]+) .+(var.|x|subsp.) ([a-z]+) "

while currentline:
    m = re.findall(regex, str(currentline))
    if m:
        for e in m:
            outputdata.append(str(e[0] + ',' + e[1]+ '\n'))
    n = re.findall(regexsub, str(currentline))
    if n:
        for f in n:
            subspdata.append(str(f[0] + ',' + f[1] + ',' + f[2] + ',' + f[3] + '\n'))
    for ra in regexalt:          
        o = re.findall(ra, str(currentline))
        if o:
            for g in o:
                altdata.append(str(g[0] + ',' + g[1]+ '\n'))
    currentline = inputfile.readline()

textfile = open('Drew1998_output.csv','w')
textfile.writelines(outputdata)
textfile.close()

textfile = open('Drew1998_output_subsp.csv','w')
textfile.writelines(subspdata)
textfile.close()

textfile = open('Drew1998_outputlong.csv','w')
textfile.writelines(altdata)
textfile.close()
            
            