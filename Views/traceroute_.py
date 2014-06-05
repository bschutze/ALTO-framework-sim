#!/usr/bin/python

#Master-Thesis dot parsing framework (TRACEROUTE MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#import pydot
import json	#for parsing edge attributes
#import pyparsing
#import pickle

#/**
# Module provides interface to analyse data.
#**/

#Finds the interfaces (edge headlabels) on the path provided. 
#@returns interfaceList a list of interfaces found on the path (strings)
def getInterfaces(edgeList,nodeList, shortestPathsDict, interfaces):
	outterDict = {}
	innerDict = {}
	vantagePoints = getVantagePoints(nodeList)
	hiddenNodes = getHiddenNodes(nodeList)	
	print "GETTING INTERFACES:"
	print nodeList
	
	for outterkey, innerDict in shortestPathsDict:
		interfaceList = []
		for innerKey, shortPath in innerDict:
			if not shortPath:
				#outterKey and innerKey are neighbors
				interfaceList = interfaces[(int(outterKey)*HASH_MULTIPLIER)+int(innerKey)]
			else:
				
				for idx, val in enumerate(shortPath):
					print idx, val
					interfaceList = interfaces[(int(shortPath[idx]))]
		
		innerDict[y] = interfaceList
	outterDict[x] = innerDict
	return outterDict
	

#takes a list of pydot node objects and parses out the names of nodes that are grouped as 'H' (hidden)
def getHiddenNodes(nodeList):
	token = "H"
	hiddenNodes = []
	for n in nodeList:
		#name = int(n.get_name())
		print token, n.get_name()
		if token == n.get_group():
			hiddenNodes.append(name)
	print "Hidden nodes:", hiddenNodes
	
#takes a list of pydot node objects and parses out the names of nodes that are grouped as 'V' (vantage-point)	
def getVantagePoints(nodeList):
	token = 'V'
	vantagePoints = []
	for n in nodeList:
		#name = int(n.get_name())
		print token, n.get_name()
		if token == n.get_group():
			vantagePoints.append(name)
	print "Vanatage Pointss:", vantagePoints


