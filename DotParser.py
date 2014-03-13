#!/usr/bin/python

#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses the djikstra algorithm implemented by David Eppstein
#execution: 
#python DotParser.py [graphname] [startNode] [endNode] [PID_grouping_threshold]
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
import pickle
from libraries.dijkstra import *

#
#Function definitions
#
#function takes a dictionary and creats a sub_dictionary within, based on supplied values
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

#iterates a list to get the keys to sum up values stored in a dict (Alto Map) 
def getTotalPathCosts(providedMap, pathList):

	total=0
	for x in range(len(pathList)-1):
		key = ((pathList[x])*100000+(pathList[x+1]))
		total = total + providedMap[key]

	return total

#find the smalles value on a path (basically used to find min bandwidth & throughput)
def getMinValue(providedMap, pathList):
	minValue=999999
	for x in range(len(pathList)-1):
		key = ((pathList[x])*100000+(pathList[x+1]))
		tempMin= providedMap[key]
		if tempMin<minValue:
			minValue=tempMin
	return minValue

#generates the sub dictionary to build the "real" cost Map. It takes a len(networkmap) 
#length List with shortest paths from one particular PID to all PID's

def genSubCostDict(constList,someCostMap):
	
	subDict = {}
	edgeCost = 0
	src = 0
	dst = 0
	shortList = constList
	
	
	for x in range(len(shortList)):
			tempList=shortList[x]
			#print "genSub tempList content: ", tempList
			#print "tempList length: ", len(tempList)
			if len(tempList)==1:
				#print "We in here!"
				edgeCost = 0
				dst = tempList.pop(0)
				#subDict[res] = edgeCost
			else:
				src = tempList.pop(0)

				while tempList:
					#if len(tempList) >=1: 
					dst = tempList.pop(0)
					#try:
					#print "SRC: ", src
					#print "DST: ", dst
					edgeCost = edgeCost + int(someCostMap[src*100000+dst])
					src = dst
				#print subDict
			#print "About to insert: ", dst
			#print "With value: ", edgeCost
			subDict[dst]=edgeCost
			edgeCost=0
			
	return subDict


#currently not used, because we are converting all .dot node names to int.
"""def genNetworkList(nodeList):
	resultNetworkMap = []
	for n in nodeList:
		name = n.get_name()
		#if (n is not "node") and (n is not "edge"):
		if not (name == "node" or name == "edge"):
		#if not name == "node" and not name == "edge":
			resultNetworkMap.append(name)
			#print name
	resultNetworkMap.sort()
	return resultNetworkMap
"""
def genBaseNetworkMap(rawNetworkMap): #Method generates the base networkmap i.e. 1 pid = 1 node
	sorted(rawNetworkMap, key = int)
	#print "Sorted: ", rawNetworkMap
	tempDict = {}
	for x in range(1, len(rawNetworkMap)+1):
		tmp = "PID"+str(x)
		tempDict[tmp]=rawNetworkMap.pop(0) #take the first item in the list
	#print tempDict
	return tempDict
		
"""
#function aggregates router ID's into PID's based on threshold
#takes 
def aggregateToPIDs(nodeHoodDict, rawCostMap, threshold):
	aggNetworkMap={}
	tempMinCost = 9999999
	tempMinNodeFirst = 9999999
	tempMinNodeSecond = 9999999
	for x in rawCostMap:
		tempDict = rawCostMap[x]
		#print "HERE COMES X: "
		#print x
		for y in range(1,len(tempDict)+1):
			#print "HERE COMES y: "
			#print y
			
			tmpMinCost = tempDict[y]
			if tmpMinCost < minCost:
				minCost = tmpCost
				tempMinNode = y
				for z in range(1, len(tempDict)+1):
					tempDict
			
				
#takes a dictionary only containing key : value pairs and returns the first key who's
#value is below the threshold
def checkForThreshold(someDict, threshold, currentPos):
	
	for x in range(currentPos,len(someDict)-currentPos):
		if(someDict[x] < threshold):
			return x
		else:
			return 0
#checks if the supplied int is in the subdict with key "node"
def isNeighbor(rawCostMap, node, neighbor):
	if neighbor in rawCostMap[node]:
		return 1
	else:
		return 0
"""	

def aggregatePids(edgeMap, threshold, hoodDict, rawCostMap):
	noMore = 1
	pidCount = 100000
	pidsContent = {}
	tmpNodeList = []
	while (noMore):
		nodeList = []
		key = getMin(edgeMap)#get the key for lowes value in dictionary
		dest = key % 100000
		src = key / 100000
		reverseKey = dest*100000+src
		if (edgeMap[key] < threshold and edgeMap[reverseKey] < threshold ):
			
			tmpNodeList.append(src)
			tmpNodeList.append(dest)
			print tmpNodeList
			del edgeMap[key]
			del edgeMap[reverseKey]
			print "entering neighborhood watch src: %d dest: %d" % (src, dest)
			if(isNeighbor(src, dest, hoodDict)):
				
		else:
			noMore=0
	



#This method takes a dictionary containing all edges (key format "src*100000+dest") as argument and returns the lowes value 
def getMin(edgeMap):
	tempMin = 999999
	minimum = 999999
	pos = 0
	for key in edgeMap: #x is all the keys in the dictionary
		tempMin = edgeMap[key]
		if tempMin<minimum:
			minimum = tempMin
			pos = key
	return pos



#def updateRawCostMap(pidName, ):
#


def isNeighbor(node1, node2, hood):
#looks in hood to see if node2 is a neighbor of node1, bool result
	temp = hood[node1]
	print temp
	for entry in temp:
		print "we are looking at: %d" % entry
		if(entry==node2):
			print "   %d is neighbor of %d" % (node2, node1)
			return 1
	print "   %d is not neighbor of %d" % (node2, node1)
	return 0



#************************************************************
####################### PROGRAM START #######################
#************************************************************

#shortest path starting & ending points
path  = str(sys.argv[1])
start = int(sys.argv[2])
end   = int(sys.argv[3])
PIDThreshold = int(sys.argv[4])

#import dot file
graph = pydot.graph_from_dot_file(path)
#grabbing the list of edges
edgeList = graph.get_edge_list()
#storing the list of nodes
nodeList = graph.get_node_list()


#Holds the nodes with its neighbors and associated edge weights
dijkstraFormatDict = {} # used for dijkstra and aggregation 

#List of all ID's used (PIDS)
#rawNetworkMap = genNetworkList(nodeList)
#print rawNetworkMap
fakenodesList = []
pathCostMap = {}	#Map with hasehd node names as key and cost as value
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
	
	fakenodesList.append(src)	#add nodes to networkmap
	fakenodesList.append(dest)	#add nodes to networkmap
	pathCostMap[(src*100000) + dest] = label
	#pathCostMap[(dest*100000) + src] = label
	delayMap[(src*100000) + dest] = int(edgeAttr['delay'])
	throughputMap[(src*100000) + dest] = int(edgeAttr['throughput'])
	latencyMap[(src*100000) + dest] = int(edgeAttr['latency'])
	bandwidthMap[(src*100000) + dest] = int(edgeAttr['bandwidth'])
	
		
#shortest path algorithm based on Dijkstra

dijk,Predecessors = Dijkstra(dijkstraFormatDict, start, end)
shortPathList = shortestPath(dijkstraFormatDict, start, end)
fakenodesList = removeDublicates(fakenodesList)


#OUTPUT
sorted(pathCostMap, key = int)
print("\n")
print "Dijkstra,  from %s to %s, has total Cost:" %(start, end), dijk[end] #D[end] is total cost
print "\nShortest path from %s to %s :" %(start, end), shortPathList
print "\nList of Nodes: ", fakenodesList
print "\nHashed Costs: ", pathCostMap
#print "\nDelay Map: ", delayMap
#print "\nThroughput Map: ", throughputMap
#print "\nLatency Map: ", latencyMap
#print "\nBandwidth Map: ", bandwidthMap


#DOING CALCULATIONS WITH THE SHORTEST PATH AND THE DIFFERENT MAPS

pathCost = getTotalPathCosts(pathCostMap, shortPathList)
print "\nPath total cost: \t",pathCost

pathDelay = getTotalPathCosts(delayMap, shortPathList)
print "\nPath total delay: \t",pathDelay

pathMinBandwidth = getMinValue(bandwidthMap, shortPathList)
print "\nPath min bandwidth: \t",pathMinBandwidth

pathLatency = getTotalPathCosts(latencyMap, shortPathList)
print "\nPath total latency: \t",pathLatency


#building a "real" Alto cost map. From all PIDs to all PID

#print dijkstraFormatDict

tempList = []
rawCostMap = {}	#lists costs from all to nodes, to all nodes
tempDict = {}
for x in range(1,len(fakenodesList)+1):
	#print "Outter: ", x
	for y in range(1,len(fakenodesList)+1):
		shortPathList = shortestPath(dijkstraFormatDict, x, y)
		tempList.append(shortPathList)
		#print "\nSpanning Tree from: %d  \t|to: %d \t|VAL: "(x,y)
		#print shortPathList
		#print "testList: ", testList
		#print "Inner: ", y
	#print "TestList: "
	#print testList
	rawCostMap[x]=genSubCostDict(tempList, pathCostMap)
	tempList = [] #clearing tempList

	#rawCostMap.append[x] = tempDict
#	print "\nTest Output: ", testList
#print "\nONE ELEMENT: ", testList.pop(0)
#print "\nONE ELEMENT: ", testList.pop(0)
#print "\nONE ELEMENT: ", testList
#test = testList[0]
#print "\nTEST: ", test
#print "CostMap: "
#print rawCostMap

costMapFile = open("ALTO_COST_MAP.txt", "w")
costMapFile.write(str(rawCostMap))
costMapFile.close()

costMapPickle = open("ALTO_COST_MAP.dat","w")
pickle.dump(rawCostMap, costMapPickle)
costMapPickle.close()

baseNetworkMap = genBaseNetworkMap(fakenodesList)
print "BASE NETWORK MAP: "
print baseNetworkMap
print "RAW COSTMAP"
print rawCostMap

print "Neighbor HOOD"
print dijkstraFormatDict

#AggNetMap = aggregateToPIDs(dijkstraFormatDict,rawCostMap, PIDThreshold)
print aggregatePids(pathCostMap, PIDThreshold, dijkstraFormatDict, rawCostMap)





