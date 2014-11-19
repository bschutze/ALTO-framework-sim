#! /usr/bin/python

#Master-Thesis dot parsing framework
#Date: 17.11.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6
#script starts the complete process to generate Data for the purpose of this thesis
#The DotParser.py is started 6 times with each GER and USA topologies (Level 0 - 6) and 4 times with the 6D_HC topology
#
#usage: python scriptStarter.py

import subprocess


print "#####################################################################"
print "##STARTING GER NETWORK###############################################"
print "#####################################################################"
#reset counter

count = 0
######0
print "starting: GER Level"+str(count)
graphName = "GER_Level"+str(count)
print graphName
graphPath = "Networks/FINAL/"+graphName+".dot"
print graphPath
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######1
print "starting:GER Level"+str(count)
graphName = "GER_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######2
print "starting: GER Level"+str(count)
graphName = "GER_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######3
print "starting: GER Level"+str(count)
graphName = "GER_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######4
print "starting: GER Level"+str(count)
graphName = "GER_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######5
print "starting: GER Level"+str(count)
graphName = "GER_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######6
print "starting: GER Level"+str(count)
graphName = "GER_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
print "done.\n"

print "#####################################################################"
print "############################STARTING USA NETWORK#####################"
print "#####################################################################"
#reset counter
count = 0
######0
print "starting: USA Level"+str(count)
graphName = "USA_Level"+str(count)
print graphName
graphPath = "Networks/FINAL/"+graphName+".dot"
print graphPath
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######1
print "starting: USA Level"+str(count)
graphName = "USA_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######2
print "starting: USA Level"+str(count)
graphName = "USA_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######3
print "starting: USA Level"+str(count)
graphName = "USA_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######4
print "starting: USA Level"+str(count)
graphName = "USA_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######5
print "starting: USA Level"+str(count)
graphName = "USA_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######6
print "starting: USA Level"+str(count)
graphName = "USA_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
print "done.\n"

print "#######################################################################"
print "##########################################STARTING 6D HC NETWORK#######"
print "#######################################################################"

#reset counter
count = 0
######0
print "starting: 6D HC Level"+str(count)
graphName = "6D_HC_Level"+str(count)
print graphName
graphPath = "Networks/FINAL/"+graphName+".dot"
print graphPath
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######1
print "starting: 6D HC Level"+str(count)
graphName = "6D_HC_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######2
print "starting: 6D HC Level"+str(count)
graphName = "6D_HC_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######3
print "starting: 6D HC Level"+str(count)
graphName = "6D_HC_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])
count = count +1
print "done.\n"
######4
print "starting: 6D HC Level"+str(count)
graphName = "6D_HC_Level"+str(count)
graphPath = "Networks/FINAL/"+graphName+".dot"
subprocess.call(["./DotParser.py",graphPath, graphName])

print "#####################################################################"
print "################################################################DONE#"
print "#####################################################################"
