#!/usr/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

# start: python networkGen.py | ./add_interfaces.py
# accesses the file Conf/networkGen_config.txt and builds network on given parameters

import sys
import ast
import time
#import subprocess


def findWeights(): #to easily change gen edge weights, just change values below(defines the weight type for all links of type: $1= A -> a, $2= A -> B, $3 = a -> b, $4= A -> C, $5 = A -> c)
	return{ "$1":100,"$2":20, "$3":10,"$4":30, "$5":100, "$6":1,}

def findSolution(x, core, agg, vp):
    return {
    	1:	{"A": core,"a": agg,"b": agg+1,"V1" : vp},
    	2:	{"A": core,"B": core+1,"a": agg,"b": agg+1,"V1" : vp},
        3:	{"A": core,"B": core+1,"C": core+2,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"V1" : vp,"V2" : vp+1},
        4:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"V1" : vp,"V2" : vp+1},
        5:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"V1" : vp,"V2" : vp+1,"V3" : vp+2},
        6:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"V1" : vp,"V2" : vp+1,"V3" : vp+2},
        8:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,"V1" : vp,"V2" : vp+1,"V3" : vp+2,"V4" : vp+3},
        9:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"I": core+8,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,"i": agg+8,"j": agg+9,"V1" : vp,"V2" : vp+1,"V3" : vp+2,"V4" : vp+3,"V5" : vp+4},
        11:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"I": core+8,"J": core+9,"K": core+10,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,"i": agg+8,"j": agg+9,"k": agg+10,"l": agg+11,"V1" : vp,"V2" : vp+1,"V3" : vp+2,"V4" : vp+3,"V5" : vp+4,"V6" : vp+5},
    }[x]

def findTemplate(x): #
    return {
	1:	("A -> a=$1\nA -> b=$5\na -> A=$1\na -> b=$3\nb -> A=$5\nb -> a=$3\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\n"),
	2:	("A -> B=$2\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\n"),
	3:	("A -> B=$2\nA -> C=$4\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> C=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\nC -> B=$2\nC -> A=$4\nC -> c=$1\nC -> d=$5\nc -> C=$1\nc -> d=$3\nd -> c=$3\nd -> C=$5\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\nc -> V2=$6\nV2 -> c=$6\nd -> V2=$6\nV2 -> d=$6\n"),
	4:	("A -> B=$2\nA -> C=$4\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> C=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> c=$1\nc -> C=$1\nc -> d=$3\nD -> C=$2\nD -> d=$1\nd -> c=$3\nd -> D=$1\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\nc -> V2=$6\nV2 -> c=$6\nd -> V2=$6\nV2 -> d=$6\n"),
	5:	("A -> B=$2\nA -> C=$4\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> C=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> c=$1\nc -> C=$1\nc -> d=$3\nD -> C=$2\nD -> E=$2\nD -> d=$1\nd -> c=$3\nd -> D=$1\nE -> C=$4\nE -> D=$2\nE -> e=$1\nE -> f=$5\ne -> E=$1\ne -> f=$3\nf -> e=$3\nf -> E=$5\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\nc -> V2=$6\nV2 -> c=$6\nd -> V2=$6\nV2 -> d=$6\ne -> V3=$6\nV3 -> e=$6\nf -> V3=$6\nV3 -> f=$6\n"),
	6:	("A -> B=$2\nA -> C=$4\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> C=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> c=$1\nc -> C=$1\nc -> d=$3\nD -> C=$2\nD -> E=$2\nD -> d=$1\nd -> c=$3\nd -> D=$1\nE -> C=$4\nE -> D=$2\nE -> F=$2\nE -> e=$1\ne -> E=$1\ne -> f=$3\nF -> E=$2\nF -> f=$1\nf -> e=$3\nf -> F=$1\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\nc -> V2=$6\nV2 -> c=$6\nd -> V2=$6\nV2 -> d=$6\ne -> V3=$6\nV3 -> e=$6\nf -> V3=$6\nV3 -> f=$6\n"),
        8:	("A -> B=$2\nA -> C=$4\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> C=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> c=$1\nc -> C=$1\nc -> d=$3\nD -> C=$2\nD -> E=$2\nD -> d=$1\nd -> c=$3\nd -> D=$1\nE -> C=$4\nE -> D=$2\nE -> F=$2\nE -> G=$4\nE -> e=$1\ne -> E=$1\ne -> f=$3\nF -> E=$2\nF -> G=$2\nF -> f=$1\nf -> e=$3\nf -> F=$1\nG -> E=$4\nG -> F=$2\nG -> H=$2\nG -> g=$1\ng -> G=$1\ng -> h=$3\nH -> G=$2\nH -> h=$1\nh -> g=$3\nh -> H=$1\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\nc -> V2=$6\nV2 -> c=$6\nd -> V2=$6\nV2 -> d=$6\ne -> V3=$6\nV3 -> e=$6\nf -> V3=$6\nV3 -> f=$6\ng -> V4=$6\nV4 -> g=$6\nh -> V4=$6\nV4 -> h=$6\n"),
	9:	("A -> B=$2\nA -> C=$4\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> C=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> c=$1\nc -> C=$1\nc -> d=$3\nD -> C=$2\nD -> E=$2\nD -> d=$1\nd -> c=$3\nd -> D=$1\nE -> C=$4\nE -> F=$2\nE -> D=$2\nE -> G=$4\nE -> e=$1\ne -> E=$1\ne -> f=$3\nF -> E=$2\nF -> G=$2\nF -> f=$1\nf -> e=$3\nf -> F=$1\nG -> E=$4\nG -> F=$2\nG -> H=$2\nG -> I=$4\nG -> g=$1\ng -> G=$1\ng -> h=$3\nH -> G=$2\nH -> I=$2\nH -> h=$1\nh -> g=$3\nh -> H=$1\nI -> G=$4\nI -> H=$2\nI -> i=$1\nI -> j=$5\ni -> I=$1\ni -> j=$3\nj -> i=$3\nj -> I=$5\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\nc -> V2=$6\nV2 -> c=$6\nd -> V2=$6\nV2 -> d=$6\ne -> V3=$6\nV3 -> e=$6\nf -> V3=$6\nV3 -> f=$6\ng -> V4=$6\nV4 -> g=$6\nh -> V4=$6\nV4 -> h=$6\ni -> V5=$6\nV5 -> i=$6\nj -> V5=$6\nV5 -> j=$6\n"),
	11:	("A -> B=$2\nA -> C=$4\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> C=$2\nB -> b=$1\n\nb -> a=$3\nb -> B=$1\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> c=$1\nc -> C=$1\nc -> d=$3\nD -> C=$2\nD -> E=$2\nD -> d=$1\nd -> c=$3\nd -> D=$1\nE -> C=$4\nE -> F=$2\nE -> D=$2\nE -> G=$4\nE -> e=$1\ne -> E=$1\ne -> f=$3\nF -> E=$2\nF -> G=$2\nF -> f=$1\nf -> e=$3\nf -> F=$1\nG -> E=$4\nG -> F=$2\nG -> H=$2\nG -> I=$4\nG -> g=$1\ng -> G=$1\ng -> h=$3\nH -> G=$2\nH -> I=$2\nH -> h=$1\nh -> g=$3\nh -> H=$1\nI -> G=$4\nI -> H=$2\nI -> J=$2\nI -> K=$4\nI -> i=$1\ni -> I=$1\ni -> j=$3\nJ -> I=$2\nJ -> K=$2\nJ -> j=$1\nj -> i=$3\nj -> J=$1\nK -> I=$4\nK -> J=$2\nK -> k=$1\nK -> l=$5\nk -> K=$1\nk -> l=$3\nl -> K=$5\nl -> k=$3\na -> V1=$6\nV1 -> a=$6\nb -> V1=$6\nV1 -> b=$6\nc -> V2=$6\nV2 -> c=$6\nd -> V2=$6\nV2 -> d=$6\ne -> V3=$6\nV3 -> e=$6\nf -> V3=$6\nV3 -> f=$6\ng -> V4=$6\nV4 -> g=$6\nh -> V4=$6\nV4 -> h=$6\ni -> V5=$6\nV5 -> i=$6\nj -> V5=$6\nV5 -> j=$6\nk -> V6=$6\nV6 -> k=$6\nl -> V6=$6\nV6 -> l=$6\n"),
    }[x]
    
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(str(i), str(j))
    return text


#numberOfNodes = str( sys.argv[1])

"""fileName = str(sys.argv[2])
outputPath = str( sys.argv[3])
"""

data = "\n"

try:
	file_handle = open('Conf/networkGen_config.txt', 'r')
except (OSError, IOError) as e:
	print e
	print "Goodbye"


for line in file_handle:
	numNodes, core, agg, vp, city = ast.literal_eval (line)
	#print "Generating network, size: %d, core: %d, agg: %d, city: %s"%(numNodes,core,agg, city)
	print "//" + city
	solution = findSolution(numNodes, core, agg, vp)
	weights = findWeights()
	#print solution
	graphTemplate = findTemplate(numNodes)
	generatedGraph = replace_all(graphTemplate, solution)
	generatedGraph = replace_all(generatedGraph, weights)
	print generatedGraph
	data = data + generatedGraph

#weights = findWeights()

#finished = replace_all(data, weights)

#print "NOW ITS AWESOME"
#print finished


#time.sleep(2)
#wrong!!!
iterList=data.split("\n")
output = ""

#for line in iterList:
#	if len(line) > 1:
#		output = output +line +"=1\n"

f = open("Conf/findPath_input.txt","w")
f.write(output)
f.close()

#subprocess.Popen(["cat", "Conf/findPath_input"])
#sys.exit(0)

