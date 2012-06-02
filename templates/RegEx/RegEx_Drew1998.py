"""Extract Genus species from Drew_1998. We are looking to find 1013 entries."""

import re

inputfile = open('Drew_1998_splist.txt')
currentline = inputfile.readline()
outputdata=[]
altdata=[]

regex = ".([A-Z][a-z]+)\s+([a-z][a-z]+\\-?[a-z]+) " #1002 entries

regexalt = ( " ([A-Z][a-z]+).+([a-z]+) ",
            ".([A-Z][a-z]+) ([a-z]+).") #1030 entries

while currentline:
    m = re.findall(regex, str(currentline))
    if m:
        for e in m:
            outputdata.append(str(e[0] + ',' + e[1]+ '\n'))
    for ra in regexalt:          
        m = re.findall(ra, str(currentline))
        if m:
            for e in m:
                altdata.append(str(e[0] + ',' + e[1]+ '\n'))  
    currentline = inputfile.readline()

textfile = open('Drew1998_output.csv','w')
textfile.writelines(outputdata)
textfile.close()

textfile = open('Drew1998_outputlong.csv','w')
textfile.writelines(altdata)
textfile.close()
            
            