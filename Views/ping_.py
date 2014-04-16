#!/usr/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6
#uses the djikstra algorithm implemented by David Eppstein

#Module does calculations to behave similar to ping, uses delay label defined in the dot file
from libraries.dijkstra import *


def getSingleValue(src, dst, edgeCostHash):
	return edgeCostHash[(src*100000)+dst]

def getPathTotal(start, end, edgeCostHash, networkDict):
	#get shortest path between start and end
	shortPathList = shortestPath(networkDict, start, end)
	print "WE PINGING SHAWTY", shortPathList


