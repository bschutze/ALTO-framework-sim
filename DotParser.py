#!/usr/bin/python

#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses the djikstra algorithm implemented by David Eppstein
#uses python 2.7.6
#execution: 
#python DotParser.py [graphname] [startNode] [endNode] [PID_grouping_threshold] [name_of_output_graph]
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

import drawGraph_
from Views import *

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

#iterates a list to get the keys to sum up values stored in a dict (Alto Map) *********PING*********?????????????????????????????
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

def aggregatePids(edgeMap, threshold, neighborHoodDict):
	noMore = 1
	pidCount = 0
	pidsContent = {}
	networkMap = {}
	tmpNodeList = []
	Round = 0
	pidName = ""
	while (noMore):
		Round+= 1
		#print "ROUND: %d PID: %s" % (Round, pidName)
		nodeList = []
		key = getMin(edgeMap)#get the key for lowes value in dictionary
		dest = key % 100000
		src = key / 100000
		reverseKey = (dest*100000)+src
		if(src == 0 and dest == 0):
			break
		#print "REMOVING: %d and: %d" % (key, reverseKey)
		if (edgeMap[key] < threshold and edgeMap[reverseKey] < threshold ):
			#print "THE EDGEMAP Leftovers: "
			#print edgeMap
			pidCount += 1
			tmpNodeList.append(src)
			tmpNodeList.append(dest)
			pidName = "PID"+str(pidCount)
			#print "Aggregated nodes: ", tmpNodeList
			del edgeMap[key]
			del edgeMap[reverseKey]
			#networkMap[pidName] = tmpNodeList
			updateHood(neighborHoodDict, src, dest)
			updateEdgeList(edgeMap, src, dest)
			updateNetworkMap(src, dest, networkMap)
			#print "\nTHE RESULTS ARE IN<<<<<<<<<<<<<<<<<<<<<<<<<8>>>>>>"
			#print neighborHoodDict
			#print "WE HAVE A NETWORKMAP: "
			#print networkMap
		else:
			noMore=0
	#print "#### FINISHED Neighborhood#### : ", neighborHoodDict
	#print "**** FINISHED NETWORKMAP  **** : ", networkMap
	return networkMap
#updates the neighborhoodDict: removes entries of aggregated devices (node2), names the aggregated nodes the value of node1, 
#and if multiple edges connect the same neighbor it keeps the cheaper
def updateHood(neighborHoodDict, node1, node2):
	#print "UPDATING HOOD: aggregating node %d and %d "% (node1, node2)
	#for x in neighborHoodDict:
		#print x, neighborHoodDict[x]
	tempDict = neighborHoodDict[node1]
	tempDict2 = neighborHoodDict[node2]
	del neighborHoodDict[node1]
	del neighborHoodDict[node2]
	del tempDict[node2]
	del tempDict2[node1]
#	print "TempDict: ", tempDict
#	print "TempDict2: ", tempDict2
	#delete entry of node joining with
	#join other entries
	#if both have the same neighbor take lower edge
#	print "AFTER"
#	print "TempDict: ", tempDict
#	print "TempDict2: ", tempDict2
	loopTempDict = tempDict.copy()
	#Delete the occurence of one another in their own 
	for key in loopTempDict:#TODO DEBUG
		if key in tempDict2:
			if tempDict[key] < tempDict2[key]:
				#print "DELETING: ", key, tempDict2[key]
				del tempDict2[key]
			else:
				#print "DELETING: ", key, tempDict[key]
				del tempDict[key]
	tempDict.update(tempDict2)
	#print "Neighbors: %d : %d contain: " % (node1, node2), tempDict
	for key in tempDict:
		#print "I AM HERE WITH VALUE: ", key
		temp = neighborHoodDict[key]
		del neighborHoodDict[key]
		loopTemp = temp.copy()
		for key2, value2 in loopTemp.items():
			#print "I am here with value: ", key2
			if node2 == key2:
				#print "I WAS HERE deleting:",key2, temp[key2]
				if node1 in loopTemp.keys():
					#print "Node %d in " % node1, loopTemp.keys()
					#print "IS %d with %d < %d with %d ?"%(node1, temp[node1], node2, temp[node2])
					if temp[node1] < temp[node2]:
						#print "now deleting: ", node2 
						del temp[node2]
					else:
						del temp[node2]
						temp[node1] = value2
				else:
					del temp[node2]
					temp[node1] = value2
		neighborHoodDict[key]=temp
	#print "result from update: "
	#print tempDict
	neighborHoodDict[node1]=tempDict
	#return neighborHood

	


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



#corrects the entries in the costMap.
#removes entries containing aggregated nodes (node2) and replaces it with the value of node1
def updateEdgeList(edgeList, node1, node2):
	loopList=edgeList
	for key, value in loopList.items():
		eNode1 = key / 100000
		eNode2 = key % 100000
		if eNode1 == node2:
			del edgeList[key]
			tmpEdge =  node1 * 100000 + eNode2
			edgeList[tmpEdge] = value
		if eNode2 == node2:
			del edgeList[key]
			tmpEdge =  eNode1 * 100000 + node1
			edgeList[tmpEdge] = value

#update the networkmap that keeps track what nodes are aggregated into pids
#checks wether aggNode is in networkMap. Stores aggNode under node.
def updateNetworkMap(node, aggNode, networkMap):
	tempList = []
	#print tempList
	if node in networkMap.keys():#if node is already present
		if aggNode in networkMap.keys():#aggNode also already
			networkMap[node].append(aggNode)
			networkMap[node] += networkMap[aggNode]
			del networkMap[aggNode]
		else:#only node is in it
			#print networkMap[node]
			tempList = networkMap[node]
			tempList.append(aggNode)
			networkMap[node] = tempList
	elif aggNode in networkMap.keys():#only aggNode is in it
		networkMap[node] = networkMap[aggNode]
		del networkMap[aggNode]
	else:#none are in it
		tempList.append(aggNode)
		tempList.append(node)
		networkMap[node]=tempList
		#print "UPDATING NETWORKMAP: ", networkMap

#This function takes a nested dictionary and changes the Keynames to PID#
def labelNetworkMap(neighborHood, networkMap):
	pidCount=1
	referenceDict={}
	loopMap = neighborHood.copy()
	tempDict={}
	missingNetMapEntries = []
	#first map PID to router ID
	for key in loopMap.keys():
		pidName = "PID"+str(pidCount)
		referenceDict[key]=pidName
		pidCount+=1
	#second replace router IDs with PIDs in neighborhood
	for key, subDict in loopMap.items():
		del neighborHood[key]
		for key2,value in subDict.items():
			tempDict[referenceDict[key2]] = value
		neighborHood[referenceDict[key]] = tempDict
		tempDict={}
	#third update networkMap (groupings what nodes belong to what PID)
	loopNetworkMap = networkMap.copy()
	for key, value in loopNetworkMap.items():
		del networkMap[key]
		networkMap[referenceDict[key]]=value
	#fourth place the missing entries, the not aggregated Nodes in networkMap
	for key, value in referenceDict.items():
		if value not in networkMap.keys():#add to networkmap
			tempList=[key]
			networkMap[value] = tempList
		#else do noting, cause node already aggregated and in networkMap
	#print "REFERENCE DICT"
	#print referenceDict
#********************************************************************
########################### PROGRAM START ###########################
#********************************************************************

#shortest path starting & ending points
path  = str(sys.argv[1])
start = int(sys.argv[2])
end   = int(sys.argv[3])
PIDThreshold = int(sys.argv[4])
graphName = str(sys.argv[5])

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
#print("\n")
#print "Dijkstra,  from %s to %s, has total Cost:" %(start, end), dijk[end] #D[end] is total cost
#print "\nShortest path from %s to %s :" %(start, end), shortPathList
#print "\nList of Nodes: ", fakenodesList
#print "\nHashed Costs: ", pathCostMap
#print "\nDelay Map: ", delayMap
#print "\nThroughput Map: ", throughputMap
#print "\nLatency Map: ", latencyMap
#print "\nBandwidth Map: ", bandwidthMap


#DOING CALCULATIONS WITH THE SHORTEST PATH AND THE DIFFERENT MAPS

pathCost = getTotalPathCosts(pathCostMap, shortPathList)
#print "\nPath total cost: \t",pathCost

pathDelay = getTotalPathCosts(delayMap, shortPathList)
#print "\nPath total delay: \t",pathDelay

pathMinBandwidth = getMinValue(bandwidthMap, shortPathList)
#print "\nPath min bandwidth: \t",pathMinBandwidth

pathLatency = getTotalPathCosts(latencyMap, shortPathList)
#print "\nPath total latency: \t",pathLatency


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
#test = testList[0]mack wilds heney
#print "\nTEST: ", test
#print "CostMap: "
#print rawCostMap

costMapFile = open("ALTO_COST_MAP_RAW.txt", "w")
costMapFile.write(str(rawCostMap))
costMapFile.close()

costMapPickle = open("ALTO_COST_MAP_RAW.dat","w")
pickle.dump(rawCostMap, costMapPickle)
costMapPickle.close()

baseNetworkMap = genBaseNetworkMap(fakenodesList)
#print "BASE NETWORK MAP: "
#print baseNetworkMap
#print "RAW COSTMAP"
#print rawCostMap

print "\n\n NODES AND NEIGHBORING NODES: ", dijkstraFormatDict

#ping_.getPathTotal(start, end, delayMap, dijkstraFormatDict)

aggNetMap = aggregatePids(pathCostMap, PIDThreshold, dijkstraFormatDict)

labelNetworkMap(dijkstraFormatDict, aggNetMap)

drawGraph_.drawGraph(dijkstraFormatDict, graphName)

print "\n AGGREGATION WITH THRESHOLD: ", PIDThreshold
print "\n ***ALTO***RESULTS***\n\n COSTMAP: ", dijkstraFormatDict
print "\n NETWORKMAP:", aggNetMap

realNetworkMap = open("ALTO_NETWORK_MAP.txt", "w")
realNetworkMap.write(str(aggNetMap))
realNetworkMap.close()

realCostMap = open("ALTO_COST_MAP.txt", "w")
realCostMap.write(str(dijkstraFormatDict))
realCostMap.close()



