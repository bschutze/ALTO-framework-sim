#!/usr/bin/python

#Master-Thesis dot parsing framework (TRACEROUTE MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6
#uses the djikstra algorithm implemented by David Eppstein

#Traceroute:
#	read out head labels from edges to represent Interfaces.
#	the % of hidden nodes needs to be connected into one cluster (hiding a certin area)
#	the % of vantage points from which traceroutes are started
#	
#Output:
#	interfaces and delay to the interface
#	

from libraries.dijkstra import *


#********************************************************************
########################### PROGRAM START ###########################
#********************************************************************

#0-100 The percentage of vantage points
vantagePercentage  = str(sys.argv[1])
#0-100 The percentage of network nodes hidden
hiddenPercentage = int(sys.argv[2])
#a dictionary in the format fit for djikstra algorithm and shortest path
neighborHood = str(sys.argv[3])


#find total number of nodes.
#calculate % hidden
#determin what nodes are interior and what nodes are exterior
#use seeded random to decide what nodes are hidden
#use same seed for determining the vantage points (ensures reproducibility)
#find shortest path from all vantage points to all nodes.
#read out and store the headlabels from the shortest "return" path (back to vantage point)
#pass data to rocketfuel script or create "traceroute" view of the network.
