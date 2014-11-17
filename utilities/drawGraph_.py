#!/local/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#this module takes a neighborhoodDict and generates a graph out of it

import pydot
from PIL import Image
#function transforms
#def transformGraphReady():
	

def drawGraph(hoodDict, grName):
	graph = pydot.Dot(label = grName, graph_type='digraph', overlap ='scale', splines ='false')
	graph.set_edge_defaults(len='4')
	#first we generate the nodes
	for key in hoodDict.keys():
		node_a = pydot.Node(str(key), shape="box")
		graph.add_node(node_a)
	for node in hoodDict.keys():
		for entry, value in hoodDict[node].items():
			edge = pydot.Edge(str(node), str(entry), label = str(value), )
			graph.add_edge(edge)
	graph.write_jpeg('Output/'+grName+'.jpeg', prog='neato')
	graph.write_dot('Output/DOT/'+grName+'.dot')
	#Image.open('Output/'+grName+'.jpeg').show()

def drawNetworkMap(netmapList, grName):
	graph = pydot.Dot(label = grName, graph_type='digraph', overlap ='scale', splines ='false')
	for key, val in netmapList.iteritems():
		name = ""+key+" |{ " 
		#print key
		#print val[0]
		#converting the set val to a list to apply list functions to it
		iterVal = list(val)
		for n in range(len(val)):
			if len (iterVal) == 1:
				name = name + str(iterVal.pop(0)) +" }"
			else:
				name = name + str(iterVal.pop(0)) +" | "
		#print name
		node = pydot.Node(label = name, shape = "record")
		node.set_name(key)
		graph.add_node(node)
		name = ""
	graph.write_jpeg('Output/'+grName+'.jpeg', prog='neato')
	graph.write_dot('Output/DOT/'+grName+'.dot')
		#struct3 [shape=record,label="hello\nworld |{ b |{c|<here> d|e}| f}| g | h"]
			
	


#method to write a traceRoute View into a dot file and jpeg
#@param	nodes	list of all found nodes
#@param	edges	list of all found edges
#@param	grName	string containing output name of graph
def drawTracerouteView(traceView, grName):
	sd_pairs = ()
	total_Edges = []
	nodes = []
	
	#FORMATING***********************************************************************
	
	#FIRST all edges have to be determined, SECOND if path is discovered, no additional entry needed!!!
	#itterating the tree to get the subtree out, i.e. the sub list (3rd level)
	for outta_key, subtree in traceView.iteritems():
		for inna_key, pathList in subtree.iteritems():
			#print "DRAWING"
			#print "outter : %d, inner: %d"%(outta_key,inna_key)
			#print pathList
			#if the list has one element
			if len(pathList) == 1:
				#if the one element is the same as the outta_key then no trace happend (src=dst)
				if pathList[0]==outta_key:
					#print "self discovered: %d and %d"%(outta_key,pathList[0])
					#build the list of nodes. Every node has a trace to itself, so best way to build node List
					nodes.append(pathList[0])
					
					#continue
				#the trace went to a neighbor node (one hop)
				else:
					if (isInListOfTuples(total_Edges, outta_key, pathList[0])==0):
						#print "Adding Real neighbors: %d and %d"%(outta_key,pathList[0])
						sd_pairs = outta_key, pathList[0]
						total_Edges.append(sd_pairs)
			#there is a list with min 2 entries and n length. divide into edge pairs starting with src node (outta_key)!
			else:
				if (isInListOfTuples(total_Edges, outta_key, pathList[0])==0):
					sd_pairs = outta_key, pathList[0]
					total_Edges.append(sd_pairs)
					#print "ADDING pairs: ", sd_pairs
				for x in range(0,len(pathList)-1):
					#print "add: %d | %d"%(pathList[x],pathList[x+1])
					if (isInListOfTuples(total_Edges, pathList[x], pathList[x+1])==0):
						sd_pairs = pathList[x],pathList[x+1]
						total_Edges.append(sd_pairs)
	#print "THE TOTAL EDGES"
	#print total_Edges
	#print "THE TOTAL NODES"
	#print nodes
	
	#DRAWING*************************************************************************
	
	graph = pydot.Dot(label = grName, graph_type='digraph', overlap ='scale', splines ='false')
	graph.set_edge_defaults(len='2')
	
	for n in nodes:
		node_a = pydot.Node(str(n), shape="box", style="filled", color="red", fillcolor="yellow")
		graph.add_node(node_a)
	for src, dest in total_Edges:
		edge = pydot.Edge(str(src), str(dest), label = str(1), )
		graph.add_edge(edge)
	graph.write_jpeg('Output/'+grName+'.jpeg', prog='neato')
	graph.write_dot('Output/DOT/'+grName+'.dot')


#draw the graph that results from the merge process. Note: Every object is one cluster
def drawMerge(pidDict, grName):
	#print "IN DRAW Func"
	graph = pydot.Dot(label = grName, graph_type='digraph', overlap ='scale', splines ='false', compound='true')
	#graph.set_edge_defaults(len='2')
	
	for pid, pidObj in pidDict.iteritems():
		#print "currently dealing with: ", pid
		#pidObj.printME()
		#generate new cluster
		cluster = pydot.Cluster(graph_name = pid, label = pid, style='filled', color='lightgrey', labelloc = "t")
		#populate cluster:
		#nodes first
		for node in set(pidObj.nodes):
			#while len(node) > 0:
			#print "Drawing: ", node
			this_node = pydot.Node(name = str(node), shape="box")
			cluster.add_node(this_node)
		for node in set(pidObj.s_nodes):
			#print "drawing Starred: ", node
			this_node = pydot.Node(name = str(node), shape="box", style = 'filled', color = 'yellow')
			cluster.add_node(this_node)
		for node in set(pidObj.a_nodes):
			#print "alias Starred: ", node
			this_node = pydot.Node(name = str(node), shape="record")
			cluster.add_node(this_node)
		for edge, weight in pidObj.in_edges.iteritems():
			src, dst = edge
			#print "Edge: ", src, dst, weight
			this_edge = pydot.Edge(str(src), str(dst), label = str(weight))
			cluster.add_edge(this_edge)
		#for edge, weight in pidObj.out_edges.iteritems():
		#	src, dst = edge
		#	print "Edge: ", src, dst, weight
		#	this_edge = pydot.Edge(str(src), str(dst), label = str(weight))
		#	cluster.add_edge(this_edge)
		cluster.set_parent_graph(graph)
		graph.add_subgraph(cluster)
	#edges connecting PIDs have to be added at the end since they don't belong into a subgraph.
	for pid, pidObj in pidDict.iteritems():
		for edge, weight in pidObj.out_edges.iteritems():
			src, dst = edge
			#print "Edge: ", src, dst, weight
			this_edge = pydot.Edge(str(src), str(dst), label = str(weight))
			graph.add_edge(this_edge)
		for dstPID, weight in pidObj.foundNeighborPIDs.iteritems():#TODO remove if practice prooves uneccesary!
			this_edge = pydot.Edge(str(pid), str(dstPID), label = str(weight))
			graph.add_edge(this_edge)
	#graph.write_jpg('Output/FIN_'+grName+'.jpg', prog='dot')#TODO neato might not render the graph right!!!
	graph.write_raw('Output/RESULTS/'+grName+'_Graph.dot')#this is what i really want, a dot file to adjust in yED graphically and to manually apply learned ALTO knowledge to it.


def makeNodeStarred(n):
	return  "*"+str(n)+"*"

def makeNodeAlias(interface, src ):
	return (str(interface)+"-"+str(src))
		

	
#function returns 1 if it found the supplied pair in the supplied list, 0 if its not in yet.				
def isInListOfTuples(ListOfTuples, src, dest):
	for i, v in enumerate(ListOfTuples):
		if (v[0] == src):
			if(v[1] == dest):
				#if edge (src --> dest) exists in tuple, return 1
				return 1
		else:
			continue
	return 0				
					
