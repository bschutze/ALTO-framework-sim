#!/usr/bin/python
#This script takes a .dot file defined network and counts the amount of edges, i.e. occurances of " -> " and parses and counts the nodes

import sys

path = str( sys.argv[1])

try:
	file_handle = open(path, 'r')
except (OSError, IOError) as e:
	print e
	print "Goodbye"

search_str = "->"
edgeCounter = 0
nodesFound = list()

for line in file_handle:
	if search_str in line:
		edgeCounter = edgeCounter +1
		needlePos = line.find(" -> ")
		posX = needlePos -3
		src = line[posX:needlePos]
		posY = needlePos+7
		dst = line[needlePos+4:posY]
		nodesFound.append(src)
		nodesFound.append(dst)
		#print "Found X: ", src
		#print "Found Y: ", dst			
		#print line
		
		
		

print "\nFile " + path +" | Number of Edges: ", edgeCounter
print ""
#print " Found Nodes: ", set(sorted(nodesFound))
print "Number of Nodes: ", len(set(nodesFound))
file_handle.close()
