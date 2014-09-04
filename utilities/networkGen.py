#!/local/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

# start: python networkGen.py parm1 | ./add_interfaces.py
# parameter = parm1 = number of backbone nodes


import sys

def findSolution(x):
    return {
    	'1':	{"A":"169","a":"370","b":"371"},
    	'2':	{"A":"153","B":"154","a":"420","b":"421"},
        '3':	{"A":"176","B":"177","C":"178","a":"460","b":"461","c":"462","d":"463"},
        '4':	{"A":"155","B":"156","C":"157","D":"158","a":"390","b":"391","c":"392","d":"393",},
        '5':	{"A":"179","B":"180","C":"181","D":"162","E":"163","a":"430","b":"431","c":"432","d":"433","e":"434","f":"435",},
        '9':	{"A":"108","B":"109","C":"110","D":"111","E":"112","F":"113","G":"114","H":"115","I":"116","a":"230","b":"231","c":"232","d":"233","e":"234","f":"235","g":"236","h":"237","i":"238","j":"239",},
    }[x]

def findTemplate(x):
    return {
    	'1':	("A -> a\nA -> b\na -> A\na -> b\nb -> A\nb -> a"),
    	'2':	("A -> B\nA -> a\na -> A\na -> b\nB -> A\nB -> b\nb -> a\nb -> B"),
        '3':	("A -> B\nA -> a\nA -> c\na -> A\na -> b\na -> C\nB -> A\nB -> b\nB -> d\nB -> C\nb -> a\nb -> B\nC -> B\nC -> a\nC -> c\nc -> A\nc -> C\nc -> d\nd -> B\nd -> c"),
        '4':	("A -> B\nA -> a\nA -> c\na -> A\na -> b\na -> C\nB -> A\nB -> C\nB -> b\nB -> d\nb -> a\nb -> B\nb -> D\nC -> B\nC -> D\nC -> a\nC -> c\nc -> A\nc -> C\nc -> d\nD -> C\nD -> b\nD -> d\nd -> c\nd -> B\nd -> D"),
        '5':	("A -> B\nA -> a\nA -> c\nA -> e\na -> A\na -> b\na -> C\na -> E\nB -> A\nB -> C\nB -> b\nB -> d\nB -> f\nb -> a\nb -> B\nb -> D\nC -> B\nC -> D\nC -> a\nC -> c\nC -> e\nc -> A\nc -> C\nc -> d\nc -> E\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nd -> c\nd -> B\nd -> D\nE -> D\nE -> a\nE -> c\nE -> e\ne -> A\ne -> C\ne -> E\ne -> f\nf -> e\nf -> B\nf -> D"),
        '9':	("A -> B\nA -> a\nA -> c\nA -> e\nA -> g\nA -> i\na -> A\na -> b\na -> C\na -> E\na -> G\na -> I\nB -> A\nB -> C\nB -> b\nB -> d\nB -> f\nB -> h\nB -> j\nb -> a\nb -> B\nb -> D\nb -> F\nb -> H\nC -> B\nC -> D\nC -> a\nC -> c\nC -> e\nC -> g\nC -> i\nc -> A\nc -> C\nc -> d\nc -> E\nc -> G\nc -> I\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nD -> h\nD -> j\nd -> c\nd -> B\nd -> D\nd -> F\nd -> H\nE -> F\nE -> D\nE -> e\nE -> g\nE -> a\nE -> c\nE -> i\ne -> E\ne -> A\ne -> C\ne -> I\ne -> f\ne -> G\nF -> E\nF -> G\nF -> b\nF -> d\nF -> j\nF -> f\nF -> h\nf -> e\nf -> F\nf -> H\nf -> B\nf -> D\nG -> F\nG -> H\nG -> e\nG -> g\nG -> a\nG -> c\nG -> i\ng -> E\ng -> G\ng -> h\ng -> A\ng -> C\ng -> I\nH -> G\nH -> I\nH -> b\nH -> d\nH -> f\nH -> h\nH -> j\nh -> g\nh -> B\nh -> D\nh -> F\nh -> H\nI -> a\nI -> c\nI -> e\nI -> g\nI -> i\ni -> A\ni -> C\ni -> E\ni -> G\ni -> I\ni -> j\nj -> i\nj -> B\nj -> D\nj -> F\nj -> H")
    }[x]
    
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


numberOfNodes = str( sys.argv[1])

"""fileName = str(sys.argv[2])
outputPath = str( sys.argv[3])

try:
	fileHandle = open(outputPath, "w")
except:(OSError, IOError) as e:
	print e
finally:
	print "Goodbye"
"""
solution = findSolution(numberOfNodes)
graphTemplate = findTemplate(numberOfNodes)
generatedGraph = replace_all(graphTemplate, solution)



	
print generatedGraph

"""
fileHandle.write(generatedGraph)
fileHandle.close()

"""



