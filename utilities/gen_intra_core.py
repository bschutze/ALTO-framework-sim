#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze

#Script generates the connections between core routers inside the pop. used to generate some of the edges (minus inter pop connection)
#that are used to calc geodetic weights via findpath.pl

import sys
import ast


def findSolution(x, core, agg):
    return {
    	2:	{"A": core,"B": core+1,"a": agg,"b": agg+1},
        3:	{"A": core,"B": core+1,"C": core+2,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3},
        4:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,},
        5:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,},
        6:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,},
        8:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,},
        9:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"I": core+8,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,"i": agg+8,"j": agg+9,},
        11:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"I": core+8,"J": core+9,"K": core+10,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,"i": agg+8,"j": agg+9,"k": agg+10,"l": agg+11},
    }[x]

def findTemplate(x):
    return {
    	2:	("A -> B=100\nB -> A=100"),
	3:	("A -> B=100\nA -> C=1\nB -> A=100\nB -> C=1\nC -> A=1\nC -> B=1"),
	4:	("A -> B=100\nA -> C=1\nB -> A=100\nB -> D=1\nC -> A=1\nC -> D=100\nD -> B=1\nD -> C=100"),
	5:	("A -> B=100\nA -> C=1\nB -> A=100\nB -> D=1\nC -> A=1\nC -> D=100\nC -> E=1\nD -> B=1\nD -> C=100\nD -> E=1\nE -> C=1\nE -> D=1"),
	6:	("A -> B=100\nA -> C=1\nB -> A=100\nB -> D=1\nC -> A=1\nC -> D=100\nC -> E=1\nD -> B=1\nD -> C=100\nD -> F=1\nE -> C=1\nE -> F=100\nF -> D=1\nF -> E=100"),
        8:	("A -> B=100\nA -> C=1\nB -> A=100\nB -> D=1\nC -> A=1\nC -> D=100\nC -> E=1\nD -> B=1\nD -> C=100\nD -> F=1\nE -> C=1\nE -> F=100\nE -> G=1\nF -> D=1\nF -> E=100\nF -> H=1\nG -> E=1\nG -> H=100\nH -> F=1\nH -> G=100\n=1"),
	9:	("A -> B=100\nA -> C=1\nB -> A=100\nB -> D=1\nC -> A=1\nC -> D=100\nC -> E=1\nD -> B=1\nD -> C=100\nD -> F=1\nE -> C=1\nE -> F=100\nE -> G=1\nF -> D=1\nF -> E=100\nF -> H=1\nG -> E=1\nG -> H=100\nG -> I=1\nH -> F=1\nH -> G=100\nH -> I=1\nI -> G=1\nI -> H=1"),
	11:	("A -> B=100\nA -> C=1\nB -> A=100\nB -> D=1\nC -> A=1\nC -> D=100\nC -> E=1\nD -> B=1\nD -> C=100\nD -> F=1\nE -> C=1\nE -> F=100\nE -> G=1\nF -> D=1\nF -> E=100\nF -> H=1\nG -> E=1\nG -> H=100\nG -> I=1\nH -> F=1\nH -> G=100\nH -> J=1\nI -> G=1\nI -> J=100\nI -> K=1\nJ -> H=1\nJ -> I=100\nJ -> K=1\nK -> I=1\nK -> J=1"),
    }[x]
    
def replace_all(text, dic):
	for i, j in dic.iteritems():
		text = text.replace(str(i), str(j))
	return text

#################################################	
	
path  = str(sys.argv[1])

try:
	file_handle = open(path, 'r')
except (OSError, IOError) as e:
	print e
	print "Goodbye"


for line in file_handle:
	numNodes, core, agg, city = ast.literal_eval (line)
	if numNodes > 1:
		#print "//" + city
		solution = findSolution(numNodes, core, agg)
		graphTemplate = findTemplate(numNodes)
		generatedGraph = replace_all(graphTemplate, solution)
		print generatedGraph
