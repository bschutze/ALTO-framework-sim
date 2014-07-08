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
	graph = pydot.Dot(label = grName, graph_type='digraph')
	graph.set_edge_defaults(len='2')
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
