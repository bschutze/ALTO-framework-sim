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
	return{ "$1":100,"$2":20, "$3":10,"$4":30, "$5":100,}

def findSolution(x, core, agg):
    return {
    	1:	{"A": core,"a": agg,"b": agg+1,},
    	2:	{"A": core,"B": core+1,"a": agg,"b": agg+1},
        3:	{"A": core,"B": core+1,"C": core+2,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3},
        4:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,},
        5:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,},
        6:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,},
        8:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,},
        9:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"I": core+8,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,"i": agg+8,"j": agg+9,},
        11:	{"A": core,"B": core+1,"C": core+2,"D": core+3,"E": core+4,"F": core+5,"G": core+6,"H": core+7,"I": core+8,"J": core+9,"K": core+10,"a": agg,"b": agg+1,"c": agg+2,"d": agg+3,"e": agg+4,"f": agg+5,"g": agg+6,"h": agg+7,"i": agg+8,"j": agg+9,"k": agg+10,"l": agg+11},
    }[x]

def findTemplate(x): #
    return {
	1:	("A -> a=$1\nA -> b=$5\na -> A=$1\na -> b=$3\nb -> A=$5\nb -> a=$3\n"),
	2:	("A -> B=$2\nA -> a=$1\na -> A=$1\na -> b=$3\nB -> A=$2\nB -> b=$1\nb -> a=$3\nb -> B=$1\n"),
	3:	("A -> B=$2\nA -> C=$4\nA -> a=$1\nA -> c=$5\na -> A=$1\na -> b=$3\na -> C=$5\nB -> A=$2\nB -> C=$2\nB -> b=$1\nB -> d=$5\nb -> a=$3\nb -> B=$1\nC -> B=$2\nC -> A=$4\nC -> a=$5\nC -> c=$1\nC -> d=$5\nc -> A=$5\nc -> C=$1\nc -> d=$3\nd -> B=$5\nd -> c=$3\nd -> C=$5\n"),
	4:	("A -> B=$2\nA -> C=$4\nA -> a=$1\nA -> c=$5\na -> A=$1\na -> b=$3\na -> C=$5\nB -> A=$2\nB -> C=$2\nB -> b=$1\nB -> d=$5\nb -> a=$3\nb -> B=$1\nb -> D=$5\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> a=$5\nC -> c=$1\nc -> A=$5\nc -> C=$1\nc -> d=$3\nD -> C=$2\nD -> b=$5\nD -> d=$1\nd -> c=$3\nd -> B=$5\nd -> D=$1\n"),
	5:	("A -> B=$2\nA -> C=$4\nA -> a=$1\nA -> c=$5\nA -> e=$5\na -> A=$1\na -> b=$3\na -> C=$5\na -> E=$5\nB -> A=$2\nB -> C=$2\nB -> b=$1\nB -> d=$5\nB -> f=$5\nb -> a=$3\nb -> B=$1\nb -> D=$5\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> a=$5\nC -> c=$1\nC -> e=$5\nc -> A=$5\nc -> C=$1\nc -> d=$3\nc -> E=$5\nD -> C=$2\nD -> E=$2\nD -> b=$5\nD -> d=$1\nD -> f=$5\nd -> c=$3\nd -> B=$5\nd -> D=$1\nE -> C=$4\nE -> D=$2\nE -> a=$5\nE -> c=$5\nE -> e=$1\nE -> f=$5\ne -> A=$5\ne -> C=$5\ne -> E=$1\ne -> f=$3\nf -> e=$3\nf -> B=$5\nf -> D=$5\nf -> E=$5\n"),
	6:	("A -> B=$2\nA -> C=$4\nA -> a=$1\nA -> c=$5\nA -> e=$5\na -> A=$1\na -> b=$3\na -> C=$5\na -> E=$5\nB -> A=$2\nB -> C=$2\nB -> b=$1\nB -> d=$5\nB -> f=$5\nb -> a=$3\nb -> B=$1\nb -> D=$5\nb -> F=$5\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> a=$5\nC -> c=$1\nC -> e=$5\nc -> A=$5\nc -> C=$1\nc -> d=$3\nc -> E=$5\nD -> C=$2\nD -> E=$2\nD -> b=$5\nD -> d=$1\nD -> f=$5\nd -> c=$3\nd -> B=$5\nd -> D=$1\nd -> F=$5\nE -> C=$4\nE -> D=$2\nE -> F=$2\nE -> a=$5\nE -> c=$5\nE -> e=$1\ne -> A=$5\ne -> C=$5\ne -> E=$1\ne -> f=$3\nF -> E=$2\nF -> b=$5\nF -> d=$5\nF -> f=$1\nf -> e=$3\nf -> B=$5\nf -> D=$5\nf -> F=$1\n"),
        8:	("A -> B=$2\nA -> C=$4\nA -> a=$1\nA -> c=$5\nA -> e=$5\nA -> g=$5\na -> A=$1\na -> b=$3\na -> C=$5\na -> E=$5\na -> G=$5\nB -> A=$2\nB -> C=$2\nB -> b=$1\nB -> d=$5\nB -> f=$5\nB -> h=$5\nb -> a=$3\nb -> B=$1\nb -> D=$5\nb -> F=$5\nb -> H=$5\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> a=$5\nC -> c=$1\nC -> e=$5\nC -> g=$5\nc -> A=$5\nc -> C=$1\nc -> d=$3\nc -> E=$5\nc -> G=$5\nD -> C=$2\nD -> E=$2\nD -> b=$5\nD -> d=$1\nD -> f=$5\nD -> h=$5\nd -> c=$3\nd -> B=$5\nd -> D=$1\nd -> F=$5\nd -> H=$5\nE -> C=$4\nE -> D=$2\nE -> F=$2\nE -> G=$4\nE -> a=$5\nE -> c=$5\nE -> e=$1\nE -> g=$5\ne -> A=$5\ne -> C=$5\ne -> E=$1\ne -> f=$3\ne -> G=$5\nF -> E=$2\nF -> G=$2\nF -> b=$5\nF -> d=$5\nF -> f=$1\nF -> h=$5\nf -> e=$3\nf -> B=$5\nf -> D=$5\nf -> F=$1\nf -> H=$5\nG -> E=$4\nG -> F=$2\nG -> H=$2\nG -> a=$5\nG -> c=$5\nG -> e=$5\nG -> g=$1\ng -> A=$5\ng -> C=$5\ng -> E=$5\ng -> G=$1\ng -> h=$3\nH -> G=$2\nH -> b=$5\nH -> d=$5\nH -> f=$5\nH -> h=$1\nh -> g=$3\nh -> B=$5\nh -> D=$5\nh -> F=$5\nh -> H=$1\n"),
	9:	("A -> B=$2\nA -> C=$4\nA -> a=$1\nA -> c=$5\nA -> e=$5\nA -> g=$5\nA -> i=$5\na -> A=$1\na -> b=$3\na -> C=$5\na -> E=$5\na -> G=$5\na -> I=$5\nB -> A=$2\nB -> C=$2\nB -> b=$1\nB -> d=$5\nB -> f=$5\nB -> h=$5\nB -> j=$5\nb -> a=$3\nb -> B=$1\nb -> D=$5\nb -> F=$5\nb -> H=$5\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> a=$5\nC -> c=$1\nC -> e=$5\nC -> g=$5\nC -> i=$5\nc -> A=$5\nc -> C=$1\nc -> d=$3\nc -> E=$5\nc -> G=$5\nc -> I=$5\nD -> C=$2\nD -> E=$2\nD -> b=$5\nD -> d=$1\nD -> f=$5\nD -> h=$5\nD -> j=$5\nd -> c=$3\nd -> B=$5\nd -> D=$1\nd -> F=$5\nd -> H=$5\nE -> C=$4\nE -> F=$2\nE -> D=$2\nE -> G=$4\nE -> e=$1\nE -> g=$5\nE -> a=$5\nE -> c=$5\nE -> i=$5\ne -> E=$1\ne -> A=$5\ne -> C=$5\ne -> I=$5\ne -> f=$3\ne -> G=$5\nF -> E=$2\nF -> G=$2\nF -> b=$5\nF -> d=$5\nF -> j=$5\nF -> f=$1\nF -> h=$5\nf -> e=$3\nf -> F=$1\nf -> H=$5\nf -> B=$5\nf -> D=$5\nG -> E=$4\nG -> F=$2\nG -> H=$2\nG -> I=$4\nG -> e=$5\nG -> g=$1\nG -> a=$5\nG -> c=$5\nG -> i=$5\ng -> E=$5\ng -> G=$1\ng -> h=$3\ng -> A=$5\ng -> C=$5\ng -> I=$5\nH -> G=$2\nH -> I=$2\nH -> b=$5\nH -> d=$5\nH -> f=$5\nH -> h=$1\nH -> j=$5\nh -> g=$3\nh -> B=$5\nh -> D=$5\nh -> F=$5\nh -> H=$1\nI -> G=$4\nI -> H=$2\nI -> a=$5\nI -> c=$5\nI -> e=$5\nI -> g=$5\nI -> i=$1\nI -> j=$5\ni -> A=$5\ni -> C=$5\ni -> E=$5\ni -> G=$5\ni -> I=$1\ni -> j=$3\nj -> i=$3\nj -> B=$5\nj -> D=$5\nj -> F=$5\nj -> H=$5\nj -> I=$5\n"),
	11:	("A -> B=$2\nA -> C=$4\nA -> a=$1\nA -> c=$5\nA -> e=$5\nA -> g=$5\nA -> i=$5\nA -> k=$5\na -> A=$1\na -> b=$3\na -> C=$5\na -> E=$5\na -> G=$5\na -> I=$5\na -> K=$5\nB -> A=$2\nB -> C=$2\nB -> b=$1\nB -> d=$5\nB -> f=$5\nB -> h=$5\nB -> j=$5\nB -> l=$5\nb -> a=$3\nb -> B=$1\nb -> D=$5\nb -> F=$5\nb -> H=$5\nb -> J=$5\nC -> A=$4\nC -> B=$2\nC -> D=$2\nC -> E=$4\nC -> a=$5\nC -> c=$1\nC -> e=$5\nC -> g=$5\nC -> i=$5\nC -> k=$5\nc -> A=$5\nc -> C=$1\nc -> d=$3\nc -> E=$5\nc -> G=$5\nc -> I=$5\nc -> K=$5\nD -> C=$2\nD -> E=$2\nD -> b=$5\nD -> d=$1\nD -> f=$5\nD -> h=$5\nD -> j=$5\nD -> l=$5\nd -> c=$3\nd -> B=$5\nd -> D=$1\nd -> F=$5\nd -> H=$5\nd -> J=$5\nE -> C=$4\nE -> F=$2\nE -> D=$2\nE -> G=$4\nE -> e=$1\nE -> g=$5\nE -> a=$5\nE -> c=$5\nE -> i=$5\nE -> k=$5\ne -> E=$1\ne -> A=$5\ne -> C=$5\ne -> I=$5\ne -> f=$3\ne -> G=$5\ne -> K=$5\nF -> E=$2\nF -> G=$2\nF -> b=$5\nF -> d=$5\nF -> j=$5\nF -> f=$1\nF -> h=$5\nF -> l=$5\nf -> e=$3\nf -> F=$1\nf -> H=$5\nf -> B=$5\nf -> D=$5\nf -> J=$5\nG -> E=$4\nG -> F=$2\nG -> H=$2\nG -> I=$4\nG -> e=$5\nG -> g=$1\nG -> a=$5\nG -> c=$5\nG -> i=$5\nG -> k=$5\ng -> E=$5\ng -> G=$1\ng -> h=$3\ng -> A=$5\ng -> C=$5\ng -> I=$5\ng -> K=$5\nH -> G=$2\nH -> I=$2\nH -> b=$5\nH -> d=$5\nH -> f=$5\nH -> h=$1\nH -> j=$5\nH -> l=$5\nh -> g=$3\nh -> B=$5\nh -> D=$5\nh -> F=$5\nh -> H=$1\nh -> J=$5\nI -> G=$4\nI -> H=$2\nI -> J=$2\nI -> K=$4\nI -> a=$5\nI -> c=$5\nI -> e=$5\nI -> g=$5\nI -> i=$1\nI -> k=$5\ni -> A=$5\ni -> C=$5\ni -> E=$5\ni -> G=$5\ni -> I=$1\ni -> K=$5\ni -> j=$3\nJ -> I=$2\nJ -> K=$2\nJ -> b=$5\nJ -> d=$5\nJ -> f=$5\nJ -> h=$5\nJ -> j=$1\nJ -> l=$5\nj -> i=$3\nj -> B=$5\nj -> D=$5\nj -> F=$5\nj -> H=$5\nj -> J=$1\nK -> I=$4\nK -> J=$2\nK -> a=$5\nK -> c=$5\nK -> e=$5\nK -> g=$5\nK -> i=$5\nK -> k=$1\nK -> l=$5\nk -> A=$5\nk -> C=$5\nk -> E=$5\nk -> G=$5\nk -> I=$5\nk -> K=$1\nk -> l=$3\nl -> B=$5\nl -> D=$5\nl -> F=$5\nl -> H=$5\nl -> J=$5\nl -> K=$5\nl -> k=$3\n"),
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
	numNodes, core, agg, city = ast.literal_eval (line)
	#print "Generating network, size: %d, core: %d, agg: %d, city: %s"%(numNodes,core,agg, city)
	print "//" + city
	solution = findSolution(numNodes, core, agg)
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

