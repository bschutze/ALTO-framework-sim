#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze

#Script adds interfaces to .dot files

import sys

path  = str(sys.argv[1])

fileHandle = open(path, 'r')

for line in fileHandle:
	#print line
	#print type(line)
	start = line.find("->")
	#print "Found at pos: ", pos
	if start > 0:
		end = line.find('\t[')
		sndEnd = line.find(',')
		print line[start-4:end]+line[end+7:sndEnd]

print "symmetrical" #enable to get symetric weights on the links
#data = fileHandle.readlines()
#pos = data.find('$')
#print pos

	
#write(str(dijkstraFormatDict))
fileHandle.close()

#print fileHandle


