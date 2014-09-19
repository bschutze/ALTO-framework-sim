#!/usr/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

# start: python networkGen.py parm1 | ./add_interfaces.py
# parameter = parm1 = number of backbone nodes


import sys
import ast
import time

def findSolution(x, core, agg):
    return {
    	1:	{"A": core,"a": agg,"b": agg+1},
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
	1:	("A -> a\nA -> b\na -> A\na -> b\nb -> A\nb -> a\n"),
	2:	("A -> B\nA -> a\na -> A\na -> b\nB -> A\nB -> b\nb -> a\nb -> B\n"),
	3:	("A -> B\nA -> C\nA -> a\nA -> c\na -> A\na -> b\na -> C\nB -> A\nB -> C\nB -> b\nB -> d\nb -> a\nb -> B\nC -> B\nC -> A\nC -> a\nC -> c\nc -> A\nc -> C\nc -> d\nd -> B\nd -> c\n"),
	4:	("A -> B\nA -> C\nA -> a\nA -> c\na -> A\na -> b\na -> C\nB -> A\nB -> C\nB -> D\nB -> b\nB -> d\nb -> a\nb -> B\nb -> D\nC -> A\nC -> B\nC -> D\nC -> a\nC -> c\nc -> A\nc -> C\nc -> d\nD -> C\nD -> B\nD -> b\nD -> d\nd -> c\nd -> B\nd -> D\n"),
	5:	("A -> B\nA -> C\nA -> a\nA -> c\nA -> e\na -> A\na -> b\na -> C\na -> E\nB -> A\nB -> C\nB -> D\nB -> b\nB -> d\nB -> f\nb -> a\nb -> B\nb -> D\nC -> A\nC -> B\nC -> D\nC -> E\nC -> a\nC -> c\nC -> e\nc -> A\nc -> C\nc -> d\nc -> E\nD -> B\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nd -> c\nd -> B\nd -> D\nE -> C\nE -> D\nE -> a\nE -> c\nE -> e\nE -> f\ne -> A\ne -> C\ne -> E\ne -> f\nf -> e\nf -> B\nf -> D\nf -> E\n"),
	6:	("A -> B\nA -> C\nA -> a\nA -> c\nA -> e\na -> A\na -> b\na -> C\na -> E\nB -> A\nB -> C\nB -> D\nB -> b\nB -> d\nB -> f\nb -> a\nb -> B\nb -> D\nb -> F\nC -> A\nC -> B\nC -> D\nC -> E\nC -> a\nC -> c\nC -> e\nc -> A\nc -> C\nc -> d\nc -> E\nD -> B\nD -> C\nD -> E\nD -> F\nD -> b\nD -> d\nD -> f\nd -> c\nd -> B\nd -> D\nd -> F\nE -> C\nE -> D\nE -> F\nE -> a\nE -> c\nE -> e\ne -> A\ne -> C\ne -> E\ne -> f\nF -> D\nF -> E\nF -> b\nF -> d\nF -> f\nf -> e\nf -> B\nf -> D\nf -> F\n"),
        8:	("A -> B\nA -> C\nA -> a\nA -> c\nA -> e\nA -> g\na -> A\na -> b\na -> C\na -> E\na -> G\nB -> A\nB -> C\nB -> D\nB -> b\nB -> d\nB -> f\nB -> h\nb -> a\nb -> B\nb -> D\nb -> F\nb -> H\nC -> A\nC -> B\nC -> D\nC -> E\nC -> a\nC -> c\nC -> e\nC -> g\nc -> A\nc -> C\nc -> d\nc -> E\nc -> G\nD -> B\nD -> C\nD -> E\nD -> F\nD -> b\nD -> d\nD -> f\nD -> h\nd -> c\nd -> B\nd -> D\nd -> F\nd -> H\nE -> C\nE -> D\nE -> F\nE -> G\nE -> a\nE -> c\nE -> e\nE -> g\ne -> A\ne -> C\ne -> E\ne -> f\ne -> G\nF -> D\nF -> E\nF -> G\nF -> H\nF -> b\nF -> d\nF -> f\nF -> h\nf -> e\nf -> B\nf -> D\nf -> F\nf -> H\nG -> E\nG -> F\nG -> H\nG -> a\nG -> c\nG -> e\nG -> g\ng -> A\ng -> C\ng -> E\ng -> G\ng -> h\nH -> F\nH -> G\nH -> b\nH -> d\nH -> f\nH -> h\nh -> g\nh -> B\nh -> D\nh -> F\nh -> H\n"),
	9:	("A -> B\nA -> C\nA -> a\nA -> c\nA -> e\nA -> g\nA -> i\na -> A\na -> b\na -> C\na -> E\na -> G\na -> I\nB -> A\nB -> C\nB -> D\nB -> b\nB -> d\nB -> f\nB -> h\nB -> j\nb -> a\nb -> B\nb -> D\nb -> F\nb -> H\nC -> A\nC -> B\nC -> D\nC -> E\nC -> a\nC -> c\nC -> e\nC -> g\nC -> i\nc -> A\nc -> C\nc -> d\nc -> E\nc -> G\nc -> I\nD -> B\nD -> C\nD -> E\nD -> F\nD -> b\nD -> d\nD -> f\nD -> h\nD -> j\nd -> c\nd -> B\nd -> D\nd -> F\nd -> H\nE -> C\nE -> F\nE -> D\nE -> G\nE -> e\nE -> g\nE -> a\nE -> c\nE -> i\ne -> E\ne -> A\ne -> C\ne -> I\ne -> f\ne -> G\nF -> D\nF -> E\nF -> G\nF -> H\nF -> b\nF -> d\nF -> j\nF -> f\nF -> h\nf -> e\nf -> F\nf -> H\nf -> B\nf -> D\nG -> E\nG -> F\nG -> H\nG -> I\nG -> e\nG -> g\nG -> a\nG -> c\nG -> i\ng -> E\ng -> G\ng -> h\ng -> A\ng -> C\ng -> I\nH -> F\nH -> G\nH -> I\nH -> b\nH -> d\nH -> f\nH -> h\nH -> j\nh -> g\nh -> B\nh -> D\nh -> F\nh -> H\nI -> G\nI -> H\nI -> a\nI -> c\nI -> e\nI -> g\nI -> i\ni -> A\ni -> C\ni -> E\ni -> G\ni -> I\ni -> j\nj -> i\nj -> B\nj -> D\nj -> F\nj -> H\n"),
	11:	("A -> B\nA -> C\nA -> a\nA -> c\nA -> e\nA -> g\nA -> i\nA -> k\na -> A\na -> b\na -> C\na -> E\na -> G\na -> I\na -> K\nB -> A\nB -> C\nB -> D\nB -> b\nB -> d\nB -> f\nB -> h\nB -> j\nB -> l\nb -> a\nb -> B\nb -> D\nb -> F\nb -> H\nb -> J\nC -> A\nC -> B\nC -> D\nC -> E\nC -> a\nC -> c\nC -> e\nC -> g\nC -> i\nC -> k\nc -> A\nc -> C\nc -> d\nc -> E\nc -> G\nc -> I\nc -> K\nD -> B\nD -> C\nD -> E\nD -> F\nD -> b\nD -> d\nD -> f\nD -> h\nD -> j\nD -> l\nd -> c\nd -> B\nd -> D\nd -> F\nd -> H\nd -> J\nE -> C\nE -> F\nE -> D\nE -> G\nE -> e\nE -> g\nE -> a\nE -> c\nE -> i\nE -> k\ne -> E\ne -> A\ne -> C\ne -> I\ne -> f\ne -> G\ne -> K\nF -> D\nF -> E\nF -> G\nF -> H\nF -> b\nF -> d\nF -> j\nF -> f\nF -> h\nF -> l\nf -> e\nf -> F\nf -> H\nf -> B\nf -> D\nf -> J\nG -> E\nG -> F\nG -> H\nG -> I\nG -> e\nG -> g\nG -> a\nG -> c\nG -> i\nG -> k\ng -> E\ng -> G\ng -> h\ng -> A\ng -> C\ng -> I\ng -> K\nH -> F\nH -> G\nH -> I\nH -> J\nH -> b\nH -> d\nH -> f\nH -> h\nH -> j\nH -> l\nh -> g\nh -> B\nh -> D\nh -> F\nh -> H\nh -> J\nI -> G\nI -> H\nI -> J\nI -> K\nI -> a\nI -> c\nI -> e\nI -> g\nI -> i\nI -> k\ni -> A\ni -> C\ni -> E\ni -> G\ni -> I\ni -> K\ni -> j\nJ -> H\nJ -> I\nJ -> K\nJ -> b\nJ -> d\nJ -> f\nJ -> h\nJ -> j\nJ -> l\nj -> i\nj -> B\nj -> D\nj -> F\nj -> H\nj -> J\nK -> I\nK -> J\nK -> a\nK -> c\nK -> e\nK -> g\nK -> i\nK -> k\nk -> A\nk -> C\nk -> E\nk -> G\nk -> I\nk -> K\nk -> l\nl -> B\nl -> D\nl -> F\nl -> H\nl -> J\nl -> k\n"),
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
	#print solution
	graphTemplate = findTemplate(numNodes)
	generatedGraph = replace_all(graphTemplate, solution)
	print generatedGraph
	data = data + generatedGraph

#time.sleep(2)

iterList=data.split("\n")
output = ""

for line in iterList:
	if len(line) > 1:
		output = output +line +"=1\n"

f = open("Conf/findPath_input.txt","w")
f.write(output)
f.close()




