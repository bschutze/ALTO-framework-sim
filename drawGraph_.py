#!/local/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#this module takes a neighborhoodDict and generates a graph out of it

import pydot

def drawGraph(hoodDict):
	graph = pydot.Dot(graph_type='digraph')
	#first we generate the nodes
	for key in hoodDict.keys():
		node_a = pydot.Node(str(key), shape="box")
		graph.add_node(node_a)
	for node in hoodDict.keys():
		for entry, value in hoodDict[node].items():
			edge = pydot.Edge(str(node), str(entry), label = str(value), )
			graph.add_edge(edge)
	graph.write_jpeg('ALTO_AGG_NET.jpeg', prog='neato')
