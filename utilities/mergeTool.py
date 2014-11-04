#!usr/bin/python

#Master-Thesis merge tool
#Date: 30.10.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#This script takes a Tracroute and an ALTO view and tries to merge them.
#Genrates statisttical information and visual

import sys
import pickle

import drawGraph_


class PID(object):

	def __init__(self, pID):
		self.netWMap = set()
		self.pid = str(pID)#string representing the name ex:  "PID2"
		self.nodes = list()#nodes that are in the traceroute and in the NW map. IMPORTANT trun it into a SET before usings!!!!
		self.a_nodes = list()#nodes that are not in NWM but in TR, nodes who's alias could not be resolved
		self.s_nodes = list()#nodes that are not in NWM but in TR, unresponsive nodes (starred)
		self.in_edges = list()#edges that connect nodes inside a PID
		self.out_edges = dict()#edges from this PID to another PID ( unidirectional, other PID has the counter part edge
		self.replaceDict = dict()#dict that keeps track of who needs to be replaced with who.
		
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
	def printME(self):
		print "\nNAME: ", self.pid
		print "NODES: ",set(self.nodes)
		print "Alias resolution failures: ", set(self.a_nodes)
		print "Starred nodes: ", set(self.s_nodes)
		print "Network Map: ", self.netWMap
		print "In edges: ", set(self.in_edges)
		print "Out edges: ", set(self.out_edges)
		print "NWM len: ", len(self.nodes)
	
	def doMagic(self):
		
		#how many nodes have been found in comparison to the NWM?
		nodes = set(self.nodes)
		diff = len(self.netWMap)-len(nodes))
		print "Do Magic"
		print diff
		if diff == 1:
			for node in self.netWMap
				if node not in nodes:
					if node in self.a_nodes:
						#replace with node from network map
					elif node in self.s_nodes: 
						#replace with node from network map
					else:
						#node just needs to be added to node
		if diff == 2:
			
		

#searches out the 
def objectManager(pidName, pidDict):
	if pidName in pidDict:
		pidObj = pidDict[pidName]
	else:
		pidObj = PID(pidName)	
	return pidObj
	
	
#method determines if the edge is inside a pid or connecting nodes outside.
def determineEdgePIDs(src, dst, pidRef):
	#print "Determin Edge Pid "
	
	
	source = trimNodes(src)	#here we have no idea about the delimiter
	destination =trimNodes(dst)
	#print "FROM TO: ", source, destination
	try:
		tmpSrcPID = pidRef[source]
		tmpDstPID = pidRef[destination]
	except KeyError:
		#"Key error" means source or destination was a vantage point(thus not in the list), so not in same PID since vps are not under ISP control. Its ok to fail silent
		#print "KEY ERROR: determineEdgePids. ", src, dst
		return False
	#return true if both are in the same PID
	#print "Edge Pids: "+tmpSrcPID +" and "+tmpDstPID
	if tmpSrcPID == tmpDstPID:
		return True
	else:
		return False
		
		
		
#method that parses nodes out of starred nodes and unresolved interfaces. !!!Results are only used as refference to find the PID of a tracerouted node!!!
def trimNodes(n, delimiter=None):
	#print "TRIM NODES: ", n
	#convert to string
	if type(n) != str:
		node = str(n)
	else:
		node = n
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
#	Include all edges found in TR. Extend if possible links where found with ALTO information

#generating statistical information
#vantage points found
vp_nodes = list()
#unresolved nodes (starr/alias)
s_nodes = list()
a_nodes = list()
edges = dict()
pidDict = dict()

HASH_MULTIPLIER = 100000

for src, subDict in tracerouteData.iteritems():

	for dst, subList in subDict.iteritems():

		if(src != dst):#if src and dst could be the same (trace to oneself)
			#for node in subList:
			edgeSrc = str(src)
			for x in range(0, len(subList)):
				reference = len(subList)
				
				if type(subList[x]) is not str:
					tmpKey = str(subList[x])
					#print "not string", node
				else:
					tmpKey = subList[x]
				
				
				 
				tmpPID = ""
				#print "NODE: ", tmpKey
				#the node is unresponsive and was entered as a *
				if tmpKey.find('*') != -1:
					solution = trimNodes(tmpKey, "*")#remove the starrs( so that we can look up what region it actually belonged to
					tmpPID = nodeToPID[solution]	#get the PID the node is assigned to
					pid = objectManager(tmpPID, pidDict)	#retrieve the right PID object
					pid.addSNode(solution)		#add to set of starred nodes (in resolved format).
					#put edge in right format and add
					if determineEdgePIDs(edgeSrc, solution, nodeToPID):
						edgeSrc = edgeSrc +"+"+ str(tmpKey)
						pid.in_edges.append(edgeSrc)
					else:
						edgeSrc = edgeSrc +"+"+ str(tmpKey)
						pid.out_edges[edgeSrc]=0
		
				#the nodes alias could not be resolved and we are dealing with a interface
				elif tmpKey.find('-') != -1:
					#d_pos = int(tmpKey.find("-"))
					solution = trimNodes(tmpKey, "-")
					tmpPID = nodeToPID[solution]
					pid = objectManager(tmpPID, pidDict)	#retrieve the right PID object or generate new
					pid.addANode(solution)		#add to list of nodes whos alias could not get resolved
					#add the edges
					if determineEdgePIDs(edgeSrc, solution, nodeToPID):
						edgeSrc = edgeSrc +"+"+ str(tmpKey)
						pid.in_edges.append(edgeSrc)
					else:
						edgeSrc = edgeSrc +"+"+ str(tmpKey)
						pid.out_edges[edgeSrc]=0			

				#the node is in the network map, so its already in the right form to look up its PID
				elif int(tmpKey) in nodeToPID:
					tmpPID = nodeToPID[int(tmpKey)]
					pid = objectManager(tmpPID, pidDict)	#retrieve the right PID object or generate new	
					pid.addNode(tmpKey)	#add to the list of nodes found.
					#add the edges
					if determineEdgePIDs(edgeSrc, tmpKey, nodeToPID):
						#print "IN edge", edgeSrc, tmpKey
						edgeSrc = edgeSrc +"+"+ str(tmpKey)
						pid.in_edges.append(edgeSrc)
					else:
						#print "OUT edge", edgeSrc, tmpKey
						edgeSrc = edgeSrc +"+"+ str(tmpKey)
						pid.out_edges[edgeSrc]=0

				else:
					
					vp_nodes = tmpKey	#vantage points are in no PID!
					
					#assigning that dst from last time is now src to determine next edge
					#edgeSrc = str(tmpKey)
				pidDict[tmpPID] = pid
				edgeSrc = str(tmpKey)

#itterate the network map to add them to the object
for key, nWM in altoNWM.iteritems():
	pid = pidDict[key]
	pid.setNWM(nWM)

#print the content of the objects
for key,obj in pidDict.iteritems():
	obj.printME()
	obj.doMagic()
	#obj.printME()








