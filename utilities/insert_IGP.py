#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 17.09.2014
#Author: Bruno-Johannes Schuetze

import sys
import ast


path = str(sys.argv[1])#the file that contains the results of findpath.pl
path2 = str(sys.argv[2])#the file on which findpath.pl was applied

needleList = list()
needleDict = dict()
output = ""

try:
	findPath_file_handle = open(path, 'r')
	coreNet_file_handle = open(path2, 'r')
except (OSError, IOError) as e:
	print e
	print "Goodbye"


for line in findPath_file_handle:
	tmp = str (line[:16])
	#tmp.split()
	#print tmp
	tmp = tmp.replace(" = ", "\",")
	tmp = "\"" + tmp
	#print tmp
	
	needle, igp_weight = ast.literal_eval (tmp)
	#needleList[needle]= line
	needleDict[needle] = str(igp_weight)
	#print needleList

name = ""

for line2 in coreNet_file_handle:
	tmp = str (line2[0:10])
	if "//" in tmp:
		name = line2
	if tmp in needleDict:
		weight = needleDict[tmp]		
		output =output + name+"\t" + line2[:18] + weight + line2[19:]
		name = ""
print output
findPath_file_handle.close()
coreNet_file_handle.close()

