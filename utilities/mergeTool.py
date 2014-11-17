#! /usr/bin/python

#Master-Thesis merge tool
#Date: 30.10.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#This script takes a Tracroute and an ALTO view and tries to merge them.
#Genrates statisttical information and visual

#usage: python utilities/mergeTool.py "grName" > "filename"
#actually starts automatically via DotParser.py

import sys
import pickle
from copy import deepcopy

import drawGraph_


class PID(object):

	def __init__(self, pID):
		self.netWMap = set()
		self.pid 		= str(pID)	#string representing the name ex:  "PID2"
		self.nodes 		= list()	#all nodes found are dumped in here. TODO: IMPORTANT trun it into a SET before usings!!!!
		self.a_nodes 		= list()	#nodes who's alias could not be resolved
		self.s_nodes 		= list()	#unresponsive nodes (starred)
		self.g_nodes		= list()	#list of all nodes found that are not starred or unresolved TODO nodes are assigned but not used... (remove?)
		self.in_edges	 	= dict()	#edges that connect nodes inside a PID
		self.out_edges	 	= dict()	#edges from this PID to another PID ( unidirectional, other PID has the counter part edge
		self.un_edges 		= dict()	#edges that have at least one member (src/dst) that is starred or unresolved
		self.foundNeighborPIDs 	= dict()	#connections to other PIDs that where added from the Cost Map since no corresponding edge was found in _edges
		self.neighbors 		= dict()	#dictionary that stores what other PIDs it is connected to and the edges that connect to that PID
		self.f_w_count 		= 0		#number of weights found and added to corresponding edge (added ALTO knowledge)
		#self.f_e_count		= 0		#number of existing edges to other PIDs discovered without associated edge in trace. (added ALTO knowledge)
		
	def addNode(self, node):
		self.nodes.append(node)
	def addOutEdge(self, edge, weight):
		self.out_edges[edge]=weight
	def addInEdge(self, edge_hash):
		self.in_edges.append(edge)
	def addSNode(self, n):
		self.s_nodes.append(n)
	def addANode(self, n):
		self.a_nodes.append(n)
	def setNWM(self, networkMap):
		self.netWMap = networkMap
	def printME(self, fhandle):
		print >>fhandle,"\nNAME: ", self.pid
		print >>fhandle,"Traced Nodes: ",self.nodes
		#print >>fhandle,"Real Nodes: ", set(self.g_nodes)
		print >>fhandle,"\tAlias resolution failures: ", self.a_nodes
		print >>fhandle,"\tStarred nodes: ", set(self.s_nodes)
		print >>fhandle,"\tALTO Network Map: ", self.netWMap
		print >>fhandle,"EDGES:"
		print >>fhandle,"\tIn edges: ", self.in_edges
		print >>fhandle,"\tOut edges: ", self.out_edges
		print >>fhandle,"\tUn-res edges: ",self.un_edges
		print >>fhandle,"\tNeighbors: ", self.neighbors
		print >>fhandle,"\tFound Cost map Neighbors: ", self.foundNeighborPIDs
		print >>fhandle,"\tNUMBER of weights dicovered via ALTO: ", self.f_w_count

	
	def doMagic(self, altoData): #only adding some stuff to make it easier to manually make changes in yED
		
		#Node replacement is only possible when:
		#	1) self.nodes is shorter that network maps content by one (only one node was not found and that)
		#	2) a nodes alias can be resolved but only if its the only node that is not present in network map, then we assume that it can be resolved.
		#Edge replacement is only possible when:
		#	1) a edge connecting PIDs is not in trace. (it can be assumed that it is there but not placed, since we have no evidence about src and 
		#	   dst node of edge)
		#	2) a edge weight can be appended if only one edge is found in the trace that connects two PIDs
		#
		
		######################################################################################################################
		#check if edge to neighbor PID exists, add if not and add only the found weight to existing (if only one edge exists)#
		######################################################################################################################
		#making a list without double entries
		tmp = set(deepcopy(self.a_nodes))
		self.a_nodes = list(tmp)
		#removing double entries
		tmpNodes = deepcopy(set(self.nodes[:]))
		self.nodes = list()
		self.nodes = deepcopy(list(tmpNodes)[:])
		print self.nodes
		
		#check if a edge to a neighboring PID was missed and add if necessary.
		neighborPidsDict = altoData[self.pid]
		for nPID, weight in neighborPidsDict.iteritems():
			#print "CHECK: new PID connections and update edge weights"
			if nPID in self.neighbors:
				tmpList = self.neighbors[nPID]
				#if there is only one edge connecting the neighbor PID
				if len(tmpList) == 1:
					#add edge weight
					#print "Adding Edge weight: ", tmpList[0], weight
					updateEdge = tmpList[0]#tmpList[0] returns the only set stored in it 
					self.out_edges[updateEdge] = weight#updating edge weight of edge connecting neighbor PID
					if updateEdge in self.un_edges:
						self.un_edges[updateEdge]=weight
						self.f_w_count = self.f_w_count + 1
					#self.out_edges[updateEdge] = weight 
			else:	#PID neighbor has not been found and a connection has to be added but just between PIDS, 
				#since we don't know the src and dst nodes of the edge.
				self.foundNeighborPIDs[nPID] = weight

		
		
		
		
		
		#########################################
		#check and sub Starred Nodes if possible#
		#########################################
		
		#assumption: we can solve a starred or unresposive node if we only have one occurance of either.

		if len(set(self.s_nodes)) == 1 and len(set(self.a_nodes)) == 0:
			print "Resolving Starr"
			#replace the starred node and edges
			needle = self.s_nodes[0]
			res_Needle = trimNodes(needle)
			
			#find and replace node in all inter PID edges (leaving the PID)
			out_edges_Iter = deepcopy(self.out_edges)
			for edge, weight in out_edges_Iter.iteritems():
				if needle in edge:
					src, dst = edge
					if type(src) is str:
						#src is the node that cant get resolved
						source = res_Needle
						destination = dst
						#adding resolved edge
						del self.out_edges[edge] #remove edge and add trimmed edge
						if src in self.nodes:
							self.nodes.remove(src)
							self.nodes.append(source)
						self.out_edges[(source,destination)]=weight
					else:
						#dst is the node that cant get resolved
						source = src
						destination = res_Needle
						del self.out_edges[edge] #remove edge and add trimmed edge
						if dst in self.nodes:
							self.nodes.remove(dst)
							self.nodes.append(destination)
						self.out_edges[(source, destination)]=weight
			
			#find and replace node in all intra PID edges (inside PID)
			
			for edge, weight in self.in_edges.iteritems():
				if needle in edge:
					src, dst = edge
					if type(src) is str:
						#src is the node that cant get resolved
						source = res_Needle
						destination = dst
						#adding resolved edge
						del self.in_edges[edge] #remove edge and add trimmed edge
						self.in_edges[(source,destination)]=weight
					else:
						#dst is the node that cant get resolved
						source = src
						destination = res_Needle
						del self.in_edges[edge] #remove edge and add trimmed edge
						self.in_edges[(source, destination)]=weight
		########################################################
		#check and sub unresolved interfaces/nodes if possible#
		########################################################
		#multiple unresolved interfaces could all be resolved into one NodeID

		elif len(self.a_nodes) > 0 and len(set(self.s_nodes)) == 0:
		
			iter_a_nodes = deepcopy(self.a_nodes)
			#replace un-resolved node and edges
			print "Its possible to resolve edge!!!"
			tempANodes = list()
			original = ""
			#loop and trimm all nodes to see if its just one node or multiple.
			for un_node in iter_a_nodes:

				tempANodes.append(trimNodes(un_node))
				original = un_node
			#if its just one node then we can substitude it
			if len(set(tempANodes)) == 1:
				#print "\tNODE: ", tempANodes
				needle = tempANodes[0] #extract the node we found
				#itterate all the edges that need replacement
				for edge, weight in self.un_edges.iteritems():
					#print "\tedge = needle?", edge, needle
					#needle should always be in edge
					if original in edge:
						
						src,dst = edge 
						#print "\tReplacing: ",src, dst
						iter_in_edges = self.in_edges
						#check if its a "in" or "out" edge:
						if edge in iter_in_edges:
							#print "\tEdge is a IN Edge\n\tRemoving: ",edge
							del self.in_edges[edge] #remove edge and add trimmed edge
							
							#its possible that scr and dst pairs in the dictionary (in_edges) come out wrong!! set = unordered!
							if type(src) is str and src.find('-') != -1:
								#src is the node that cant get resolved
								#removing the un_resolved and wrongly falsly added interface
								if src in self.nodes:
									#print "\t\tremoving from list of Nodes: ",src
									self.nodes.remove(src)
								source = trimNodes(src)
								destination = dst
								#adding resolved edge
								#print "\tAdding: ",(source,destination)
								#print "\t\tAdding to list of Nodes: ", source
								self.in_edges[(source,destination)]=weight
								#adding resolved node back to the list off all nodes
								self.nodes.append(source)
							elif type(dst) is str and dst.find('-') != -1:
								#dst is the node that cant get resolved
								#removing the un_resolved and wrongly falsly added interface
								if dst in self.nodes:
									#print "\t\tremoving from list of Nodes: ",src
									self.nodes.remove(dst)
								source = src
								destination = trimNodes(dst)
								#print "\tAdding: ",(source,destination)
								#print "\t\tAdding to list of Nodes: ", destination
								self.in_edges[(source, destination)]=weight
								#adding resolved node back to the list off all nodes
								self.nodes.append(destination)
						iter_out_edges = self.out_edges
						#else edge has to be in out_nodes and the same as above has to be done
						if edge in iter_out_edges:
							#print "\tEdge is a OUT Edge\n\tRemoving: ",edge
							del self.out_edges[edge] #remove edge and add trimmed edge
						
							#its possible that scr and dst pairs in the dictionary (in_edges) come out wrong!! set = unordered!
							if type(src) is str and src.find('-') != -1:
								#src is the node that cant get resolved
								#removing the un_resolved and wrongly falsly added interface
								if src in self.nodes:
									#print "\t\tremoving from list of Nodes: ",src
									self.nodes.remove(src)

								source = trimNodes(src)
								destination = dst
								#adding resolved edge
								#print "\tAdding: ",(source,destination)
								#print "\t\tAdding to list of Nodes: ", source
								self.out_edges[(source,destination)]=weight
								#adding resolved node back to the list off all nodes
								self.nodes.append(source)
								
								iterDict = deepcopy(self.neighbors)
								#check if the edge is connecting another PID (which it mostly should)
								for neighborPid, edgeList in iterDict.iteritems():
									tmpEdgeList = edgeList
									#print "IS EDGE IN LIST?: ", edge, edgeList
									if edge in tmpEdgeList:
										#print type(edge)
										edgeList.remove(edge)
										newEdge = set([source,destination])
										#print "FOUND adding: ", newEdge
										edgeList.append(newEdge)
									self.neighbors[neighborPid] = edgeList
								
							elif type(dst) is str and dst.find('-') != -1:
								#dst is the node that cant get resolved
								#removing the un_resolved and wrongly falsly added interface
								if dst in self.nodes:
									#print "\t\tremoving from list of Nodes: ",src
									self.nodes.remove(dst)
								source = src
								destination = trimNodes(dst)
								#print "\tAdding: ",(source,destination)
								#print "\t\tAdding to list of Nodes: ", destination
								self.out_edges[(source, destination)]=weight
								#adding resolved node back to the list off all nodes
								self.nodes.append(destination)

								iterDict = deepcopy(self.neighbors)
								#check if the edge is connecting another PID (which it mostly should)
								for neighborPid, edgeList in iterDict.iteritems():
									tmpEdgeList = edgeList
									#print "IS EDGE IN LIST?: ", edge, edgeList
									if edge in tmpEdgeList:
										#print type(edge)
										edgeList.remove(edge)
										newEdge = (source,destination)
										#print "FOUND adding: ", newEdge
										edgeList.append(newEdge)
									#add the list back to object
									self.neighbors[neighborPid] = edgeList
		
		
		tmpNodes = set(self.nodes[:])
		self.nodes = list()
		self.nodes = list(tmpNodes)[:]
		#print "THE RESOLVED NODE LIST: ", self.nodes		

		#look if the content of the cost map is represented here. if object has a neighbor, check if it found all
		#if possible, integrate unfound connection and add weight, else just add weight.
	#generate stats:
	#		How many nodes found vs not found
	#		How many nodes found are starred ofind('-') != -1r no alias res
	#		
	def genStats(self):
		print "NUMBER NODES FOUND IN TR + ALTO: ", len(self.nodes)
		tmpNodes = deepcopy(self.nodes)
		#starred nodes need to be removed (since we actually did not find them)
		for x in self.s_nodes:
			if x in tmpNodes:
				tmpNodes.remove(x)
		print "After removing Starrs: ", len(set(tmpNodes))
		numNodesFound	= len(set(tmpNodes))
		#interior edges + exterior edges + edges we know exist
		numEdgesFound	= len(self.in_edges) + len(self.out_edges)+ len(self.foundNeighborPIDs)
		return numNodesFound, numEdgesFound, self.f_w_count 

#searches out the 
def objectManager(pidName, pid_Dict):
	if pidName == '':
		print "Omanager ERROR: ", pidName
	if pidName in pid_Dict:
		pidObj = pid_Dict[pidName]
		#print "return: "+pidName
	else:
		pidObj = PID(pidName)
		#print "create: "+pidName
	return pidObj
	
		
#method that parses nodes out of starred nodes and unresolved interfaces. !!!Results are only used as refference to find the PID of a tracerouted node!!!
def trimNodes(n, delimiter=None):
	#print "TRIM NODES: ", n
	#convert to string
	if type(n) == str:
		node = n
	else:
		node = str(n)
	#is the delimiter set? if not set.		
	if delimiter == None:
		x = node.find("*")
		y = node.find("-")
		if x > -1:
			delimiter = "*"
		elif y > -1:
			delimiter = "-"
		else:
			return int(node)
	#two kinds of delimiters: * and - need to be handeled / parsed seperatly.	
	if delimiter == "*":
		s_pos = int(node.find("*"))+1
		e_pos = int(node.find("*",s_pos+1))
		return  int(node[s_pos:e_pos])
	if delimiter == "-":
		d_pos = node.find("-")
		ret = int(node[1:d_pos])
		return ret
	else:#we should never get here since there are only two delimiters! But if I get here I want to know.
		print "Error in trimNodes(): wrong delimiter!"



################################################################################################################
#startstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstart#
#startstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstartstart#
################################################################################################################

graphName  = str(sys.argv[1])
#outputPath = str(sys.argv[2])


#this script works on the data objects generated by DotParser.py 
pathTR 		= "Objects/TR_pickle.obj"
pathALTO	= "Objects/ALTO_pickle.obj"
pathNWM		= "Objects/ALTO_NWM_pickle.obj"
pathNodeToPID	= "Objects/node_to_pid_pickle.obj"

tracerouteData = pickle.load( open( pathTR, "r"))
altoData = pickle.load(open(pathALTO, "r"))
altoNWM = pickle.load( open( pathNWM, "r"))
nodeToPID = pickle.load(open( pathNodeToPID, "r"))

nodesFound = list()
edgeHash = dict()


nodesFound.append(tracerouteData.keys())


#Statistics:
#NODES: count all nodes (without starred and alias res) include network maps content to extend regular, show how much  alias res adds to that and how much unverified
#	where found via network map.
#EDGES:	count all edges from traceroute (without edges that happen due to alias resolution), show how many alias resolution edges where found. 
#	find out if PIDs are small enough to provide additional edges. (get nodes from PIDs look if traceroute found edges bewteen PIDs if not look at cost map)

#Visual:generate subgraphs based on PIDs content. Include all nodes that have been found via TR and nodes that where resolved with ALTO information. 
#	Include all edges found in TR. Extend if possible links where found with ALTO information.
#this script generates a .dot file that can be edited in yEd or other software

#generating statistical information
#vantage points found
vp_nodes = list()
#unresolved nodes (starr/alias)
s_nodes = list()
a_nodes = list()
edges = dict()
pidDict = {}

HASH_MULTIPLIER = 100000

un_check = False

for srcVP, subDict in tracerouteData.iteritems():
	for dstVP, subList in subDict.iteritems():
		#if src and dst could be the same (trace to oneself)
		if(srcVP != dstVP):
			#for node in subList:
			src = srcVP
			rawSrc = srcVP
			for n in subList:
				
				dst = trimNodes(n)		#flatten node from "*100*"/"100-200" to 100
				rawDst = n
				#determine what PID to assign the nodes and edges to
				if dst == dstVP or dst == subList[-1]:	#i the case that src is a VP
					thePID = nodeToPID[src]
				elif dst not in nodeToPID:
					thePID = nodeToPID[src]
				else:
					thePID = nodeToPID[dst]
				
				
				
				#if dst in nodeToPID:			
				#	thePID = nodeToPID[dst]
				#elif src in nodeToPID:
				#	thePID = nodeToPID[src]
				#else:
				#	print "ERROR: No PID was determined. line 215 mergeTool.py!!!"
				
				pid = objectManager(thePID, pidDict)	#retrieve the right PID object

				#sorting the node into corresponding lists
				if rawDst in nodeToPID:
					pid.addNode(rawDst)		#add to the list of nodes found.
					if type(n) is int:	#should a(rawSrlways be type int
						pid.g_nodes.append(rawDst)
				
				elif str(rawDst).find('*') != -1:
					pid.addNode(rawDst)
					pid.addSNode(rawDst)		#add to set of starred nodes (in resolved format).

				elif str(rawDst).find('-') != -1:
					pid.addNode(rawDst)
					pid.addANode(rawDst)		#add to list of nodes whos alias could not get resolved

				else:
					vp_nodes = int(rawDst)		#vantage points are in no PID
				
				#sorting the edges
				
				if type(rawDst) is str or type(rawSrc) is str:
					pid.un_edges[(rawSrc, rawDst)] = 0
				
				if src in nodeToPID and dst in nodeToPID:
					srcPid = nodeToPID[src]
					dstPid = nodeToPID[dst]
					if srcPid == dstPid:		#edge is not a edge to a neighbor
						pid.in_edges[(rawSrc,rawDst)]=0

							
					else:				#edge is a edge going to a neighbor
						pid.out_edges[(rawSrc,rawDst)]=0 # if its a incoming or out going edge is not important
						
						if srcPid in pid.neighbors.keys():
							tmp = pid.neighbors[srcPid]
							if (rawSrc,rawDst) not in tmp:	#to not add dublicates
								tmp.append((rawSrc,rawDst))
								pid.neighbors[srcPid] = tmp
							
						
						if srcPid not in pid.neighbors.keys():	#since the PID of the src node 
							tmp = [(rawSrc,rawDst)]#create new list containing tuples
							pid.neighbors[srcPid]=tmp
					
					
					
				elif src in nodeToPID and dst not in nodeToPID:#edge goes from node to VP
					pid.out_edges[(rawSrc,rawDst)]=0
				
				elif src not in nodeToPID and dst in nodeToPID:#edge goes from VP to node
					pid.out_edges[(rawSrc,rawDst)]=0
				
				
				else:					#
					print "ERROR: sorting edges, neither node is in a PID. mergeTool.py!!!"
				
				#assigning that dst from last time is now src to determine next edge (dst becomes src every new itteration)
				pidDict[thePID] = pid
				src = dst
				rawSrc = rawDst

#itterate the network map to add them to the object
#del pidDict['']#for some unexplained reason a '' empty slot is created... Here we remove it.
#print "KEYS OF PIDs:", pidDict.keys()
#adding network map of each PID to the onject representing that PID
missedPID = "PIDs not in trace but in Cost Map:\n"
pidCount = 0

for key, nWM in altoNWM.iteritems():
	if key in pidDict:
		pid = pidDict[key]
		pid.setNWM(nWM)
	else:
		missedPID = missedPID + key + "\n"
		pidCount = pidCount +1

#every missed PID means at least 1 node and 2 links (out / in)
missedPID = missedPID +"Missed PIDS: %d (added *3 to total to make up for missed PIDs)\n\n\n"%(pidCount)
pidCount = pidCount*3


totalNumNodes = 0
totalNumEdges = 0
totalNotFound = 0
totalWeightsFound = 0

fhandle = open("Output/RESULTS/" + graphName +"_MergeResults.txt", "w")

#print the content of the objects, doing merging work, generating stats.
for key,obj in pidDict.iteritems():

	obj.doMagic(altoData)
	#obj.printME(fhandle)
	tmpNumNodes, tmpNumEdges, tmpWeightsFound = obj.genStats()
	
	totalNumNodes = totalNumNodes + tmpNumNodes
	totalNumEdges = totalNumEdges + tmpNumEdges
	totalWeightsFound = totalWeightsFound + tmpWeightsFound
	totalNotFound = totalNotFound + (len(obj.netWMap)- tmpNumNodes)
	
	#print >>fhandle, "\nPID: " + obj.pid 
	#print >>fhandle, "Nodes Traced: %d, Nodes in NWM: %d, Diff = %d"%(tmpNumNodes, len(obj.netWMap),len(obj.netWMap)-tmpNumNodes)
	#print >>fhandle, "Edges Traced: %d,"%(tmpNumEdges)

print >>fhandle, "\nTotal items revealed: " + str(totalNumNodes+totalNumEdges+totalWeightsFound+pidCount)
print >>fhandle, "Total Number of Nodes Found: " + str(totalNumNodes) 
print >>fhandle, "Total Number of Edges Found: "+str(totalNumEdges)
print >>fhandle, "Total Number Edge Weights discovered: ", totalWeightsFound
print >>fhandle, "\nTotal Number of Nodes in Network Map but not in Trace: ", totalNotFound
print >>fhandle, missedPID

for key,obj in pidDict.iteritems():
	obj.printME(fhandle)

drawGraph_.drawMerge(pidDict, graphName)#generate .dot file of graph to be edited in yED (the graph drawn up by neato etc is horrible)

#closing open file handle
fhandle.close()



