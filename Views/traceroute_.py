#!/usr/bin/python

#Master-Thesis dot parsing framework (TRACEROUTE MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

import pydot
import json	#for parsing edge attributes
import copy
from utilities import file_interfaces_

#from utilities import drawTracerouteView
#import pyparsing
#import pickle

#/**
# Module generates based on certain data structures a view of the network that should represent tracerout measurements from vantage points
#**/

#Method generates the Traceroute View of the graph. We list the headlabels on the shortest path and apply alias resolution
#TODO we are resolving all interfaces, as long as node is not marked hidden
#@returns a tree structure representing the traceroute view of the network
def genTracerouteView(aliasResMap, latencyMap, nodeList, shortestPathsDict, interfaces, graphName):
	#print "GEN TRACEROUTE:"
	#print shortestPathsDict
	tree = shortestPathsDict
	HASH_MULTIPLIER = 100000
	outterDict = {}
	innerDict = {}
	#variables for drawing traceroute view
	nodesFound = []
	edgesFound = []
	#total latency between src and target
	total_latency = 0.0
	#string containing all latency for write to file
	text_total_latency = ""
	#string for latency inbetween nodes
	text_latency = ""
	#processing delay constant, used per transit and recipient node (2ms)
	processing_delay = 2.0
	#starCounter = 1 #counts the number of times a unresponsive node is found. Counter is appended to the name.
	#src and target for the interface trace
	vantagePoints = getVantagePoints(nodeList) #the list of vantage points from where we collect interfaces(headlabels)
	targets = vantagePoints
	hiddenNodes = getHiddenNodes(nodeList) #the list of nodes that will not appear in the trace
	starredNodes = getStarredNodes(nodeList)#the list of nodes that will appear as * in the trace
	#print "Subing node names for Interfaces"
	for src in vantagePoints:
		for target in targets:
			#processing_delay = 2.0
			temp_inter=[]
			#print "Building new Tree with source: %d  \t|target: %d \t|"%(src,target)
			#extracting the list of the intermediate nodes
			tempVPs = ((tree[src])[target])
			#print tempVPs
			text_latency = "Path %d  ->  %d\t via: %s\n"%(src, target, tempVPs)
			if len(tempVPs) == 1:
				temp_inter = tempVPs

			else:
				for key in range(len(tempVPs)-1):
					#print "LENGTH: ", len(tempVPs)-1
					#print "KEY: ", key
					first=tempVPs[key]
					#print "FIRST: ", first
					#print "Adding"
					#print first
					second = tempVPs[key+1]
					#print "SECOND: ", second
					#print second
					#Adding up the total latency between src and target.
					#text_latency = text_latency + str(latencyMap[(first*HASH_MULTIPLIER)+second])
					total_latency = total_latency +processing_delay + latencyMap[(first*HASH_MULTIPLIER)+second]
					
					
					#when targeting a hidden node, omit from trace,
					if second in hiddenNodes:
						temp = processing_delay + latencyMap[(first*HASH_MULTIPLIER)+second]
						text_latency = text_latency +"From: "+str(first)+" to hidden: "+str(second)+" = "+str(temp)+"\n"
						continue
					if second in starredNodes:
						tmpVal = interfaces[(first*HASH_MULTIPLIER)+second]
						#print "Interface: ", tmpVal
						#slice the string to only get first charackter
						t_head, sep, tail = tmpVal.partition('-')
						#trimming the first charackter in this case: "
						head = t_head[1:]
						temp_inter.append('*'+str(head)+'*')
						#print "Starred: *" +  str(head)+'*'
						
						text_latency = text_latency +"From: "+str(first)+" to starred: "+str(second)+" = "+str(latencyMap[(first*HASH_MULTIPLIER)+second]+processing_delay)+"\n"
						continue
					#check if alias resulution is possible on edge
					aliResTest = aliasResMap[(first*HASH_MULTIPLIER)+second]
					#if alias can be resolved
					if aliResTest == 1:
						tmpVal = interfaces[(first*HASH_MULTIPLIER)+second]
						#print "Interface: ", tmpVal
						#slice the string to only get first charackter
						t_head, sep, tail = tmpVal.partition('-')
						#trimming the first charackter in this case: "
						head = t_head[1:]
						#print "Adding: ", head
						temp_inter.append(int(head))
						edgesFound.append(int(head))
						#print "Normal: ", head
						text_latency = text_latency +"From: "+str(first)+" to: "+str(second)+" = "+str(latencyMap[(first*HASH_MULTIPLIER)+second]+processing_delay)+"\n"
					else:
						temp_inter.append(interfaces[(first*HASH_MULTIPLIER)+second])
						text_latency = text_latency +"From: "+str(first)+" to alias: "+(interfaces[(first*HASH_MULTIPLIER)+second])
						text_latency = text_latency +" = "+str(latencyMap[(first*HASH_MULTIPLIER)+second]+processing_delay)+"\n"
						#print "Encountered ALIAS RESULUTION NO!:", interfaces[(first*HASH_MULTIPLIER)+second]
						#print temp_interfaces
						
			#print "Adding interfaces: ", temp_inter
			innerDict[target] = copy.deepcopy(temp_inter)
			#print "INNER DICT LOADING WITH:"
			#print innerDict
			#Adding the latency for the complete path into a String to written to a file
			text_total_latency += text_latency
			text_total_latency = text_total_latency+"Path Total: "+str(total_latency)+"\n\n"
			total_latency = 0.0
			
		outterDict[src] = copy.deepcopy(innerDict)
	#print "\n\nHERE"
	#print outterDict
	file_interfaces_.writeToFile(text_total_latency,graphName)
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
		outter[first]= copy.deepcopy(inner)
	print "\n\n*******************************"
	print outter
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


#takes a list of pydot node objects and parses out the names of nodes that are grouped as 'S' (star nodes that show up as * in the trace)
def getStarredNodes(nodeList):
	token = 'S'
	starredNodes = []
	for n in nodeList:
		#most .dot files have settings for drawing nodes and edges and thus have to be handled, ex: node [shape=box]; edge [len=2];
		if n.get_name() is 'node':
			continue
		if n.get_name() is 'edge':
			continue
		name = int(n.get_name())
		#print token, n.get_name()
		if token == n.get_group():
			starredNodes.append(name)
	#print "Vanatage Pointss:", vantagePoints
	return starredNodes

