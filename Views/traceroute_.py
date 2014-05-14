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
import random
import sys
#import pydot
import json	#for parsing edge attributes
#import pyparsing
#import pickle

def trace(edgeList, nodeList, hPercentage, xSeed):
	print "\nSTARTING TRACEROUTE: Traceroute_.py\n"
	print hPercentage
	hNodes = []
	numNodes = len(nodeList)
	a = float(numNodes)/100
	print a
	numHidden = (float(numNodes)/100*hPercentage)
	print "Number of nodes: %d num hidden: %d" % (numNodes, numHidden)
	for x in range (1, int(numHidden+1)):
		random.seed(xSeed)
		hNodes.append(random.randint(1,numNodes))
		print hNodes
		#del numNodes[random.randint(1,numNodes)]
		xSeed += 3
	print "TYPE: ", type(hNodes)
	countEdgesPerNode(edgeList, nodeList)
	return hNodes

def countEdgesPerNode(edgeList, nodeList):
	edgeCount=[]
	for edge in edgeList:
		edgeCount.append(int(edge.get_source()))
		edgeCount.append(int(edge.get_destination()))
	print "NODES EDGES COUNT"
	print edgeCount
	for node in nodeList:
		count = edgeCount.count(node)
		print "Node: ", int(node)
		print "Count: ", count

#********************************************************************
########################### PROGRAM START ###########################
#********************************************************************



#find total number of nodes.
#calculate % hidden
#determin what nodes are interior and what nodes are exterior
#use seeded random to decide what nodes are hidden
#use same seed for determining the vantage points (ensures reproducibility)
#find shortest path from all vantage points to all nodes.
#read out and store the headlabels from the shortest "return" path (back to vantage point)
#pass data to rocketfuel script or create "traceroute" view of the network.


