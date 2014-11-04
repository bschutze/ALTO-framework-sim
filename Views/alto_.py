#!/usr/bin/python

#Master-Thesis dot parsing framework
#Date: 08.10.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6
#Generates the alto view of network defined in .dot format (requires a specific network configuration)

import sys
import copy

# Generates the complete cost map that contains costs from each PID to all PID's
# @parm all_shortestPaths nested dict containing the shortest paths from all to all
# @parm pid_refMap dictionary containing the mapping between node names and PID numbers
# @parm path_cost_map a dictionary containing all edges and associated weights/costs
# @returns a complete ALTO cost map with all costs from all to all
def genFullAltoCostMap(all_shortestPaths, pid_refMap, path_cost_map):
	#print "GEN_FULL_ALTO_MAP"
	#print all_shortestPaths
	#print pid_refMap
	#print path_cost_map
	full_cost_map = dict()

	for o_src, subDict in all_shortestPaths.iteritems():
		temp_partial_cost_map = dict()
		costs = 0
		#print "Loop 1: ", o_src
		for i_src, subList in subDict.iteritems():
		#	print "Loop, O_src =", o_src, " i_src = ", i_src, " ", subList
			#we filter out only entries that are not related via same PID
			if pid_refMap[o_src] != pid_refMap[i_src]:
				#if the subList only contains one entry its the shortest path to itself, so uninterresting
				if len(subList) == 1:
		#			print "I SHOULD NEVER GET HERE"
					continue
				
				#take 2nd entry (1st entry src, 2nd dest) 
				if len(subList) == 2:
					key = (o_src *100000)+i_src
					temp_partial_cost_map[i_src] = path_cost_map[key]
		#			print "adding (len 2): {%s :{ %s : %s}"%(o_src,i_src,path_cost_map[key])
			
				if len(subList) > 2:
					#print "HUHU"
					for index, item in enumerate(subList):
						#if end of list not reached and the item is not of the same pid as the i_src (not neccesary to have costs of inter PID links)
						if index < len(subList)-1 and pid_refMap[item] != pid_refMap[subList[index+1]]:
		#					print "INDEX: ", index,
		#					print "length subList: ", len(subList)
							key = (item *100000)+subList[index+1]
		#					print "", (item *100000)+subList[index+1], " = ", path_cost_map[key]
							costs = costs + path_cost_map[key]
		#			print "adding (len?): {%s :{ %s : %s}"%(o_src,i_src,costs)
					temp_partial_cost_map[i_src] = costs
					costs = 0
		full_cost_map[o_src]=copy.deepcopy(temp_partial_cost_map)
	
	#print "\nCost map might just be done!!!: "
	#print full_cost_map
	#print "\n"
	return full_cost_map

#takes a PID neighborhood cost map and formates it such that it can be used 



	
	
#building the alto network map. Grouping all nodes marked with the same PID# from the .dot file.
# @returns a dictionary with stings as keys ('PID1'), with sets of nodes contained in that PID, as the value. This is the ALTO network map
# @returns a dictionary for PID lookup used to build the costMap ( {node : PID, ....} )
def makeNetworkMap(altoDict):
	networkMap = dict()
	for key, value in altoDict.iteritems():
		#PID0 was used as a independent PID... PID0 is the PID of the vantage points, disregard
		if (value != 'PID0'):	
			if not value in networkMap:
				networkMap[value] = set()
			networkMap[value].add(key)
	#print "THE NETWORKMAP: ", networkMap
	return networkMap

def genAltoCostMap(pid_ref, neighborHood):
	#print "GEN ALTO COST MAP:"
	#print neighborHood
	#print "PID reference: ", pid_ref
	neighbor_cost_map  = dict()
	cost_map_edges = dict()
	#tmp_cost_vals = dict()
	#tempHood = copy.deepcopy(neighborHood)
		
	#loop through the the neighbors
	for key, subDict in neighborHood.iteritems():
		tmp_cost_vals = dict()
	#	print "Outter KEY: %s , outter VAL: %s"%(key, subDict)
		#check if key is in the list, vantage points are invalid keys!
		if key not in pid_ref:
			continue
		#get the PID 
		outter_pid_number = pid_ref[key]
		#check if the pid number already exsists. If it doesn exist just do normal add, i.e start a new dictionary and add neighbors
		if outter_pid_number not in neighbor_cost_map:# and outter_pid_number != 'PID0':
			#itterate sub dictionary ( add the neighbors(iKey) with costs (iValue)
			for iKey, iVal in subDict.iteritems():
				if iKey not in pid_ref:
					continue
				#filter out if outter PID is trying to save a path to it self, i.e. PID1 to PID1 =10...s
				if(pid_ref[iKey] != outter_pid_number):
	#				print "\tAdding first timer: %s -- %s = %s"%(outter_pid_number,pid_ref[iKey],iVal)
					tmp_cost_vals[pid_ref[iKey]] = iVal
				#else:
					#continue
	#				print "\tskipping: %s : %s"%(iKey,iVal)
			
		#else check wether connection to neighbor exsists. If yes keep cheaper weights. If not just add to the list of neighbors
		#only append the neighbors ( if already exist, keep lower edge weight )
		else:
			existing_PID_entry = neighbor_cost_map[outter_pid_number]
			for iKey, iVal in subDict.iteritems():
	#			print "\t%s=%s already exists"% (pid_ref[iKey],iVal)
	#			print "\t in: ", neighbor_cost_map
				#check if key is in list (vantage points i.e. PID0 are ignored here
				if iKey not in pid_ref:
					continue
				
				
				#if it already exists add only if weight is lower
				if pid_ref[iKey] in existing_PID_entry:
					#print "IT IS IN IT", existing_PID_entry[pid_ref[iKey]]
					if (existing_PID_entry[pid_ref[iKey]] > iVal):
	#					print "\tupdating : %s = %s with %s"%(pid_ref[iKey], existing_PID_entry[pid_ref[iKey]],iVal)
						tmp_cost_vals[pid_ref[iKey]] = iVal
	#					print "\tupdated: ", tmp_cost_vals
				elif (pid_ref[iKey] != outter_pid_number):
					tmp_cost_vals[pid_ref[iKey]] = iVal
					
	#				print "\tno update, %s: %s"%(pid_ref[iKey], iVal)
	#				print "\t", tmp_cost_vals
						
		#copy from the temp list to make permanent
	#	print "LOOP END with: %s : %s"%(outter_pid_number,key)
	#	print "FINAL ADD OF THE LOOP:", tmp_cost_vals
		
		#if this is a update to already existing entry
		if outter_pid_number in neighbor_cost_map:
			temp = neighbor_cost_map[outter_pid_number]
			temp.update(tmp_cost_vals)
			neighbor_cost_map[outter_pid_number] = copy.deepcopy(temp)
		#else just add the thing
		else:
			neighbor_cost_map[outter_pid_number] = copy.deepcopy(tmp_cost_vals)


	#	print "\nThis round we have: ", neighbor_cost_map
	#	print "\n"
	#END FOR LOOP
	#print "\nFINALLY THE ENDRESULT: ", neighbor_cost_map
	return neighbor_cost_map
