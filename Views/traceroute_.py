#!/usr/bin/python

#Master-Thesis dot parsing framework (TRACEROUTE MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

import pydot
import json	#for parsing edge attributes
import copy

#from utilities import drawTracerouteView
#import pyparsing
#import pickle

#/**
# Module generates based on certain data structures a view of the network that should represent tracerout measurements from vantage points
#**/

#Method generates the Traceroute View of the graph. We list the headlabels on the shortest path and apply alias resolution
#TODO we are resolving all interfaces, as long as node is not marked hidden
#@returns a tree structure representing the traceroute view of the network
def genTracerouteView(aliasResMap,nodeList, shortestPathsDict, interfaces):
	tree = shortestPathsDict
	HASH_MULTIPLIER = 100000
	outterDict = {}
	innerDict = {}
	#variables for drawing traceroute view
	nodesFound = []
	edgesFound = []
	#src and target for the interface trace
	vantagePoints = getVantagePoints(nodeList) #the list of vantage points from where we collect interfaces(headlabels)
	targets = vantagePoints
	hiddenNodes = getHiddenNodes(nodeList) #the list of nodes that will not appear in the trace	
	#print "Subing node names for Interfaces"
	for src in vantagePoints:
		for target in targets:
			temp_inter=[]
			#print "Building new Tree with source: %d  \t|target: %d \t|"%(src,target)
			#extracting the list of the 
			tempVPs = ((tree[src])[target])
			#print tempVPs
			#testStuff = removeHiddenNodes(hiddenNodes, tempVPs) TODO this is not the right way. rework
			if len(tempVPs) == 1:
				temp_inter = tempVPs
			else:
				for key in range(len(tempVPs)-1):
					first=tempVPs[key]
					#print first
					second = tempVPs[key+1]
					#print second
					#when targeting a hidden node, omit from trace,
					if second in hiddenNodes:
						#print "Encountered hidden node: ", second
						continue
					#check if alias resulution is possible on edge
					aliResTest = aliasResMap[(first*HASH_MULTIPLIER)+second]
					#if alias can be resolved
					if aliResTest == 1:
						tmpVal = interfaces[(first*HASH_MULTIPLIER)+second]
						#slice the string to only get first charackter
						t_head, sep, tail = tmpVal.partition('-')
						#trimming the first charackter in this case: "
						head = t_head[1:]
						temp_inter.append(int(head))
						edgesFound.append(int(head))
					else:
						temp_inter.append(interfaces[(first*HASH_MULTIPLIER)+second])
						#print temp_interfaces
			#print "Adding interfaces: ", temp_inter
			innerDict[target] = temp_inter
			#print "INNER DICT LOADING WITH:"
			#print innerDict
		outterDict[src] = copy.deepcopy(innerDict)
	return outterDict

#method that creates a neighborhood view of the traceroute shortest path traces, only the result from genTracerouteView() is needed
def genTracerouteNeighborhood(traceView):
	outter = {}
	neighbors = []
	for first, subtree in traceView.iteritems():
		inner  = {}
		for second, daList in subtree.iteritems():
			#print "WE IN HERE: ", first
			#print "We in here: ", second
			#print "we still deh: ", daList
			if first == second:
				continue
			elif len(daList) == 1:
				#print "First: %d, second %d", (first, second)
				#print "adding: ", daList[0]
				#print "LIST: ", daList
				#length = len(daList)
				#print "length: ", length
				inner[daList[0]] = 1
		outter[first]=inner
	return outter



	

#takes a list of pydot node objects and parses out the names of nodes that are grouped as 'H' (hidden)
def getHiddenNodes(nodeList):
	token = "H"
	hiddenNodes = []
	for n in nodeList:
		#most .dot files have settings for drawing nodes and edges and thus have to be handled, ex: node [shape=box]; edge [len=2];
		if n.get_name() is 'node':
			continue
		if n.get_name() is 'edge':
			continue
		name = int(n.get_name())
		#print token, n.get_name()
		if token == n.get_group():
			hiddenNodes.append(name)
	#print "Hidden nodes:", hiddenNodes
	return hiddenNodes
	
#takes a list of pydot node objects and parses out the names of nodes that are grouped as 'V' (vantage-point)	
def getVantagePoints(nodeList):
	token = 'V'
	vantagePoints = []
	for n in nodeList:
		#most .dot files have settings for drawing nodes and edges and thus have to be handled, ex: node [shape=box]; edge [len=2];
		if n.get_name() is 'node':
			continue
		if n.get_name() is 'edge':
			continue
		name = int(n.get_name())
		#print token, n.get_name()
		if token == n.get_group():
			vantagePoints.append(name)
	#print "Vanatage Pointss:", vantagePoints
	return vantagePoints
"""
#essentially wrong, because edges to node 5 still exist... I have to remove it after collecting the interfaces.
def removeHiddenNodes(nodesH, listOfNodes):
	for node in nodesH:
		if node in listOfNodes:
			print "ON THE INSIDE"
			print node
			print listOfNodes
			print "afer deletion: "
			listOfNodes.remove(node)
			print listOfNodes
	return listOfNodes
	
#method 
def aliasResolution(aliasResMap, HASH_MULTI, src, dest):
	tmp = aliasResMap[(src*HASH_MULTI)+dest]
	#print "ALIAS RESOLUTION: ", tmp
	return tmp
"""
