#!/usr/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#Module does calculations to behave similar to ping

def ping(src, dst, edgeCostHash):
	return edgeCostHash[(src*100000)+dst]

def doThePing(edgeCostHash):
	
