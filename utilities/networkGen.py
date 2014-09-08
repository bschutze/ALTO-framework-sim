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
    	'1':	{"A":"135","a":"290","b":"291"},
    	'2':	{"A":"153","B":"154","a":"420","b":"421"},
        '3':	{"A":"165","B":"166","C":"167","a":"370","b":"371","c":"372","d":"373"},
        '4':	{"A":"139","B":"140","C":"141","D":"142","a":"310","b":"311","c":"312","d":"313",},
        '5':	{"A":"150","B":"151","C":"152","D":"153","E":"182","a":"340","b":"341","c":"342","d":"343","e":"344","f":"345",},
        '6':	{"A":"130","B":"131","C":"132","D":"133","E":"134","F":"180","a":"280","b":"281","c":"282","d":"283","e":"284","f":"285",},
        '8':	{"A":"118","B":"119","C":"120","D":"121","E":"122","F":"123","G":"124","H":"125","a":"250","b":"251","c":"252","d":"253","e":"254","f":"255","g":"256","h":"257",},
        '9':	{"A":"108","B":"109","C":"110","D":"111","E":"112","F":"113","G":"114","H":"115","I":"116","a":"230","b":"231","c":"232","d":"233","e":"234","f":"235","g":"236","h":"237","i":"238","j":"239",},
        '11':	{"A":"143","B":"144","C":"145","D":"146","E":"147","F":"148","G":"149","H":"150","I":"151","J":"152","K":"153","a":"320","b":"321","c":"322","d":"323","e":"324","f":"325","g":"326","h":"327","i":"328","j":"329","k":"330","l":"331"},
    }[x]

def findTemplate(x):
    return {
    	'1':	("A -> a\nA -> b\na -> A\na -> b\nb -> A\nb -> a"),
    	'2':	("A -> B\nA -> a\na -> A\na -> b\nB -> A\nB -> b\nb -> a\nb -> B"),
        '3':	("A -> B\nA -> a\nA -> c\na -> A\na -> b\na -> C\nB -> A\nB -> b\nB -> d\nB -> C\nb -> a\nb -> B\nC -> B\nC -> a\nC -> c\nc -> A\nc -> C\nc -> d\nd -> B\nd -> c"),
        '4':	("A -> B\nA -> a\nA -> c\na -> A\na -> b\na -> C\nB -> A\nB -> C\nB -> b\nB -> d\nb -> a\nb -> B\nb -> D\nC -> B\nC -> D\nC -> a\nC -> c\nc -> A\nc -> C\nc -> d\nD -> C\nD -> b\nD -> d\nd -> c\nd -> B\nd -> D"),
        '5':	("A -> B\nA -> a\nA -> c\nA -> e\na -> A\na -> b\na -> C\na -> E\nB -> A\nB -> C\nB -> b\nB -> d\nB -> f\nb -> a\nb -> B\nb -> D\nC -> B\nC -> D\nC -> a\nC -> c\nC -> e\nc -> A\nc -> C\nc -> d\nc -> E\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nd -> c\nd -> B\nd -> D\nE -> D\nE -> a\nE -> c\nE -> e\ne -> A\ne -> C\ne -> E\ne -> f\nf -> e\nf -> B\nf -> D"),
        '6':	("A -> B\nA -> a\nA -> c\nA -> e\na -> A\na -> b\na -> C\na -> E\nB -> A\nB -> C\nB -> b\nB -> d\nB -> f\nb -> a\nb -> B\nb -> D\nb -> F\nC -> B\nC -> D\nC -> a\nC -> c\nC -> e\nc -> A\nc -> C\nc -> d\nc -> E\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nd -> c\nd -> B\nd -> D\nE -> D\nE -> a\nE -> c\nE -> e\ne -> A\ne -> C\ne -> E\ne -> f\nF -> b\nF -> d\nF -> f\nf -> e\nf -> B\nf -> D\nf -> F"),
        '8':	("A -> B\nA -> a\nA -> c\nA -> e\nA -> g\na -> A\na -> b\na -> C\na -> E\na -> G\nB -> A\nB -> C\nB -> b\nB -> d\nB -> f\nB -> h\nb -> a\nb -> B\nb -> D\nb -> F\nb -> H\nC -> B\nC -> D\nC -> a\nC -> c\nC -> e\nC -> g\nc -> A\nc -> C\nc -> d\nc -> E\nc -> G\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nD -> h\nd -> c\nd -> B\nd -> D\nd -> F\nd -> H\nE -> D\nE -> F\nE -> a\nE -> c\nE -> e\nE -> g\ne -> A\ne -> C\ne -> E\ne -> f\ne -> G\nF -> E\nF -> G\nF -> b\nF -> d\nF -> f\nF -> h\nf -> e\nf -> B\nf -> D\nf -> F\nf -> H\nG -> F\nG -> H\nG -> a\nG -> c\nG -> e\nG -> g\ng -> A\ng -> C\ng -> E\ng -> G\ng -> h\nH -> G\nH -> b\nH -> d\nH -> f\nH -> h\nh -> g\nh -> B\nh -> D\nh -> F\nh -> H"),
        '9':	("A -> B\nA -> a\nA -> c\nA -> e\nA -> g\nA -> i\na -> A\na -> b\na -> C\na -> E\na -> G\na -> I\nB -> A\nB -> C\nB -> b\nB -> d\nB -> f\nB -> h\nB -> j\nb -> a\nb -> B\nb -> D\nb -> F\nb -> H\nC -> B\nC -> D\nC -> a\nC -> c\nC -> e\nC -> g\nC -> i\nc -> A\nc -> C\nc -> d\nc -> E\nc -> G\nc -> I\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nD -> h\nD -> j\nd -> c\nd -> B\nd -> D\nd -> F\nd -> H\nE -> F\nE -> D\nE -> e\nE -> g\nE -> a\nE -> c\nE -> i\ne -> E\ne -> A\ne -> C\ne -> I\ne -> f\ne -> G\nF -> E\nF -> G\nF -> b\nF -> d\nF -> j\nF -> f\nF -> h\nf -> e\nf -> F\nf -> H\nf -> B\nf -> D\nG -> F\nG -> H\nG -> e\nG -> g\nG -> a\nG -> c\nG -> i\ng -> E\ng -> G\ng -> h\ng -> A\ng -> C\ng -> I\nH -> G\nH -> I\nH -> b\nH -> d\nH -> f\nH -> h\nH -> j\nh -> g\nh -> B\nh -> D\nh -> F\nh -> H\nI -> a\nI -> c\nI -> e\nI -> g\nI -> i\ni -> A\ni -> C\ni -> E\ni -> G\ni -> I\ni -> j\nj -> i\nj -> B\nj -> D\nj -> F\nj -> H"),
        
        '11':	("A -> B\nA -> a\nA -> c\nA -> e\nA -> g\nA -> i\nA -> k\na -> A\na -> b\na -> C\na -> E\na -> G\na -> I\nB -> A\nB -> C\nB -> b\nB -> d\nB -> f\nB -> h\nB -> j\nB -> l\nb -> a\nb -> B\nb -> D\nb -> F\nb -> H\nb -> J\nC -> B\nC -> D\nC -> a\nC -> c\nC -> e\nC -> g\nC -> i\nC -> k\nc -> A\nc -> C\nc -> d\nc -> E\nc -> G\nc -> I\nD -> C\nD -> E\nD -> b\nD -> d\nD -> f\nD -> h\nD -> j\nD -> l\nd -> c\nd -> B\nd -> D\nd -> F\nd -> H\nd -> J\nE -> F\nE -> D\nE -> e\nE -> g\nE -> a\nE -> c\nE -> i\nE -> k\ne -> E\ne -> A\ne -> C\ne -> I\ne -> f\ne -> G\nF -> E\nF -> G\nF -> b\nF -> d\nF -> j\nF -> f\nF -> h\nF -> l\nf -> e\nf -> F\nf -> H\nf -> B\nf -> D\nf -> J\nG -> F\nG -> H\nG -> e\nG -> g\nG -> a\nG -> c\nG -> i\nG -> k\ng -> E\ng -> G\ng -> h\ng -> A\ng -> C\ng -> I\nH -> G\nH -> I\nH -> b\nH -> d\nH -> f\nH -> h\nH -> j\nH -> l\nh -> g\nh -> B\nh -> D\nh -> F\nh -> H\nh -> J\nI -> a\nI -> c\nI -> e\nI -> g\nI -> i\nI -> k\ni -> A\ni -> C\ni -> E\ni -> G\ni -> I\ni -> j\nJ -> I\nJ -> K\nJ -> b\nJ -> d\nJ -> f\nJ -> h\nJ -> j\n J ->l\nj -> i\nj -> B\nj -> D\nj -> F\nj -> H\nj -> J\nK -> J\nK -> a\nK -> c\nK -> e\nK -> g\nK -> i\nK -> k\nk -> A\nk -> C\nk -> E\nk -> G\nk -> I\nk -> K\nk -> l\nl -> B\nl -> D\nl -> F\nl -> H\nl -> J"),
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




