#!/usr/bin/python

#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses the djikstra algorithm implemented by David Eppstein
#execution: python DotParser.py [graphname] [startNode] [endNode]
"""DOT FILE
graph Test {
	node [shape=box]
	edge [len=2]
	overlap=false
	1 -- 2[label=3];
	1 -- 3[label=4];
	1 -- 5[label=2];
	2 -- 3[label=2];
	2 -- 4[label=5];
	3 -- 4[label=1];
}
"""



import sys
import pydot
import pyparsing
from libraries.dijkstra import *


#function takes a dictionary and creats a sub_dictionary within based on supplied values
def insertEdge(outerDict, key1, key2, value):
	innerDict = {}


	if key1 in outerDict:
		innerDict = outerDict[key1]
		innerDict[key2] = value
		outerDict[key1] = innerDict
	else:
		innerDict[key2] = value
		outerDict[key1] = innerDict

#removes dublicates from a list
def removeDublicates(seq):
	keys = {}
	for s in seq:
		keys[s] = 1
	return keys.keys()


#prog start
#shortest path starting & ending points
path  = str(sys.argv[1])
start = int(sys.argv[2])
end   = int(sys.argv[3])

#import dot file
graph = pydot.graph_from_dot_file(path)
#grabbing the list of edges
edgeList = graph.get_edge_list()

betterDict = {}	#Holds the nodes with its neighbors and associated edge weights
networkmap = [] #List of all ID's used (PIDS)
costmap = {}	#Map with hasehd PID's as key and cost as value

"""
#hashing the values //NOT USED
for e in edgeList:
	srcEdge = e.get_source()
	destEdge = e.get_destination()
	label=e.get_label()
	intSrcEdge = int(srcEdge)
	intDestEdge= int(destEdge)
	intLabel = int(label)
	
	dictionary[(intSrcEdge*100000) + intDestEdge]=intLabel
"""
#BUILDING NETWORK AND COST MAP!!!!-----------------------------------------

#storing in dictionary
for e in edgeList:
	#tempDict.clear()	
	src   = int(e.get_source())
	dest  = int(e.get_destination())
	label = int(e.get_label())
	insertEdge(betterDict, src, dest, label)
	insertEdge(betterDict, dest, src, label)
	networkmap.append(src)	#add nodes to networkmap
	networkmap.append(dest)	#add nodes to networkmap
	costmap[(src*100000) + dest] = label

#print betterDict
	
#shortest path algorithm based on Dijkstra

dijk,Predecessors = Dijkstra(betterDict, start, end)
result = shortestPath(betterDict, start, end)
networkmap = removeDublicates(networkmap)

print("\n")
print("Dijkstra,  from %s to %s, has total Cost:" %(start, end))
print dijk[end]	#D[end] is total cost
print("\n")
print("Shortest path from %s to %s" %(start, end))
print result
print("\n")
print("Network Map:")
print networkmap
print("\n")
print("Cost Map:")
print costmap
print("\n")



	
#print pids




