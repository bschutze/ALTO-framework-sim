#!/usr/bin/python

#Master-Thesis dot parsing framework (TRACEROUTE MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#This script reads node names out of a text file and tries to find them in a dot file defining a network.
#In the .dot file it will add annotations to the nodes, marking them as vantagepoints or hidden nodes.
#@param path and name of the file to draw the hidden nodes from
#@param path and name of the .dot file to be modified.

import sys

nodesPath = str(sys.argv[1])
dotPath = str(sys.argv[2])
#open file read only mode
nodesFile = open(nodesPath, 'r')
#open file read and write
dotFile = open(dotPath, 'r+')


nodesToHide = []
#read a line from the file object

nodesToHide.append(nodesFile.readline())



with open(nodesPath) as nodesFile:
	for line in nodesFile:
		print line
