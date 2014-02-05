#!/usr/bin/python

#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses the djikstra algorithm implemented by David Eppstein
#execution: python DotParser.py [graphname] [startNode] [endNode]
"""DOT FILE FORMAT
graph Test {
	node [shape=box]
	edge [len=2]
	overlap=false
	1 -- 2[label=3, bandwidth=20, delay = 2, latency=2, throughput=17];
...
}
"""



import sys
import pydot
import pyparsing
import json
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

#itterates a list and 
def getTotalPathCosts(providedMap, pathList):

	total=0
	for x in range(len(pathList)-1):
		key = ((pathList[x])*100000+(pathList[x+1]))
		total = total + providedMap[key]

	return total


#prog start
#shortest path starting & ending points
path  = str(sys.argv[1])
start = int(sys.argv[2])
end   = int(sys.argv[3])

#import dot file
graph = pydot.graph_from_dot_file(path)
#grabbing the list of edges
edgeList = graph.get_edge_list()

dijkstraFormatDict = {}	#Holds the nodes with its neighbors and associated edge weights
networkmap = [] #List of all ID's used (PIDS)
costmap = {}	#Map with hasehd PID's as key and cost as value
#attributes = []	#List of all attributes

latencyMap 	= {} #
bandwidthMap 	= {} #
throughputMap 	= {} 
delayMap   	= {}

#BUILDING NETWORK AND COST MAP!!!!-----------------------------------------

#parsing and splitting up into all the different maps
for e in edgeList:
	#tempDict.clear()	
	src   = int(e.get_source())
	dest  = int(e.get_destination())
	label = int(e.get_label())
	
	tempAttr = json.dumps(e.get_attributes())
	edgeAttr = json.loads(tempAttr)

	insertEdge(dijkstraFormatDict, src, dest, label)
	insertEdge(dijkstraFormatDict, dest, src, label)
	
	networkmap.append(src)	#add nodes to networkmap
	networkmap.append(dest)	#add nodes to networkmap
	costmap[(src*100000) + dest] = label
	delayMap[(src*100000) + dest] = int(edgeAttr['delay'])
	throughputMap[(src*100000) + dest] = int(edgeAttr['throughput'])
	latencyMap[(src*100000) + dest] = int(edgeAttr['latency'])
	bandwidthMap[(src*100000) + dest] = int(edgeAttr['bandwidth'])
	
		
#shortest path algorithm based on Dijkstra

dijk,Predecessors = Dijkstra(dijkstraFormatDict, start, end)
shortPathList = shortestPath(dijkstraFormatDict, start, end)
networkmap = removeDublicates(networkmap)


#OUTPUT

print("\n")
print("Dijkstra,  from %s to %s, has total Cost:" %(start, end))
print dijk[end]	#D[end] is total cost
print("\n")
print("Shortest path from %s to %s" %(start, end))
print shortPathList
print("\n")
print("Network Map:")
print networkmap
print("\n")
print("Cost Map:")
print costmap
print("\n")
print("Delay Map:")
print delayMap
print("\nThroughput Map")
print throughputMap
print("\nLatency Map:")
print latencyMap
print("\nBandwidth Map:")
print bandwidthMap


#DOING CALCULATIONS WITH THE SHORTEST PATH AND THE DIFFERENT MAPS

#iterate result list from shortest path algorithms to get pairs for the hashed key values
total=0

result = getTotalPathCosts(costmap, shortPathList)
print result

result = getTotalPathCosts(delayMap, shortPathList)
print result

