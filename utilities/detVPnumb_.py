#!/usr/bin/python

#Master-Thesis dot parsing framework (determine amount of VPs module MODULE)
#Date: 25.10.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#/**
#This module generates statistics about the impact a increasing number of Vanatge Points has on the number of links discovered
#selects 100 times different combinations of vantage points
#**/

import random
from utilities import file_interfaces_
from Views import traceroute_


#Method generates the Traceroute View of the graph. We list the headlabels on the shortest path and apply alias resolution

#@returns 
def genVpStatistics(nodeList, shortestPathsDict, graphName):
	print "generating statistics about the optimal number of Vantage Points for the graph\n"
	#print shortestPathsDict
	HASH_MULTIPLIER = 100000

	#string containing all latency for write to file
	text_total_links = "Number_of_Vantage_Points\tNumber_of_Links\n0\t0\n1\t0\n"
	vPs = traceroute_.getVantagePoints(nodeList) #the list of vantage points from where we collect interfaces(headlabels)
	tmpPathAverage = 0
	averageLinksFound = 0
	#print vPs
	#TODO remove?
	#hiddenNodes = traceroute_.getHiddenNodes(nodeList) #the list of nodes that will not appear in the trace
	#starredNodes = traceroute_.getStarredNodes(nodeList)#the list of nodes that will appear as * in the trace
	
	numbVPs = 2 # determines how many Vantage points are to be used
	
	#run as many times as there are vantage points
	while(numbVPs<=len(vPs)):
		#print "New Round, Number of VPs: ", numbVPs
		tmpPathAverage = 0
		linksFound = list()
		#links found during itteration
		#loop number of samples required times
		for numb in range(0,1000):
			#print "Iteration Nr: ", numb
			linksFound = list()
			vantagePoint = list()

			#generate list of randomly vantage points to run traces to/ from
			#if(numbVPs != len(vPs)):
				#vantagePoints = getRandVantagePoints(vPs, numbVPs)
			#else:
				#vantagePoints = vPs
			tmp = shuffleVPs(vPs)
			vantagePoints = tmp[:numbVPs]
			#targets = vantagePoints
			#loop list to get all possible starting points
			for src in vantagePoints:
				#floop list to get all possible destinations
				for target in vantagePoints:
					#print "From %s to %s"%(src, target)
					#skipp if I'm tracing to myself
					if src == target:
						continue
					#extract the path
					temp = shortestPathsDict[src]
					tempVPs = temp[target]
					#if length is 1 its trying to trace to itself (should not be possible)
					#if len(tempVPs) == 1:
						#continue
						#linksFound.append((src*HASH_MULTIPLIER)+target) #has the src and dest to represent the directed edge
					#hash the found edge and append to list of liks found
					for key in range(len(tempVPs)-1):
						#print "Here: ",tempVPs
						first=tempVPs[key]
						second = tempVPs[key+1]
						#Adding up the edges between src and target.
						linksFound.append((first*HASH_MULTIPLIER)+second)
			tmpPathAverage = tmpPathAverage + len(set(linksFound))
			#print "VPs: %s: number of edges: %d"%(str(vantagePoints),len(set(linksFound)))
			#print "set of links found: ", len(set(linksFound))
		averageLinksFound = averageLinksFound + float(float(tmpPathAverage)/1000)
		#print "Average : ", averageLinksFound
		text_total_links = text_total_links + "" + str(numbVPs) + "\t" + str(averageLinksFound) + "\n"
		averageLinksFound = 0
		numbVPs = numbVPs + 1

	file_interfaces_.writeLinkCount(text_total_links,graphName)
	print "done"
	return text_total_links



	
#takes a list off all available vantage points and returns number
def getRandVantagePoints(vpList, number):
	randVPs = []
	count = 0
	while(count <= number):
		tmp = random.choice(vpList)
		randVPs.append(tmp)
		count = count + 1
	return randVPs
# 2nd approach, shuffel list and return
def shuffleVPs(array):
        random.shuffle(array)
        return array
