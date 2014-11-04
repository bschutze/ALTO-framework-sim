#!/usr/bin/python
#This script takes a .dot file defined network and counts the amount of edges, i.e. occurances of " -> " in it

import sys

path = str( sys.argv[1])

try:
	file_handle = open(path, 'r')
except (OSError, IOError) as e:
	print e
	print "Goodbye"

search_str = "->"
counter = 0

for line in file_handle:
	if search_str in line:
		counter = counter +1

print "\nFile " + path +" | Number of Edges: ", counter
print ""
file_handle.close()
