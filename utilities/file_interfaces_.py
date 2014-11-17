#!/local/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#this module takes a neighborhoodDict and generates a graph out of it


def writeToFile(toFile, name, ):
	
	f = open("Output/TRACEROUTE/"+name+"_Latency.txt", "w")
	f.write(toFile)
	f.close()

def writeLinkCount(toFile, name):
	f = open("Output/VANTAGE_POINTS/"+name+"_vpStats.txt", "w")
	f.write(toFile)
	f.close()
	
def writeTRStats(toFile, name):
	f = open("Output/RESULTS/TR_stats_"+name+".txt", "w")
	f.write(toFile)
	f.close()
