#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 
#Author: Bruno-Johannes Schuetze

#Script parses dot file (takes off meta) and adds =1. Output is input for findPath.pl!!!

import sys

path  = str(sys.argv[1])

fileHandle = open(path, 'r')

for line in fileHandle:
	#print line
	#print type(line)
	start = line.find("->")
	pos = line.find("\t")
	#print "Found at pos: ", pos
	if pos == 0:
		if start > 0:
			end = line.find('\t[')
			sndEnd = line.find(',')
			#print line[start-4:end]+line[end+7:sndEnd] //TODO this is the working version
			print line[pos+1:end]+line[end+7:sndEnd]

print "symmetrical" #enable to get symetric weights on the links
#data = fileHandle.readlines()
#pos = data.find('$')
#print pos

	
#write(str(dijkstraFormatDict))
fileHandle.close()

#print fileHandle


