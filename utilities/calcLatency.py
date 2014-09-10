#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 09.09.2014
#Author: Bruno-Johannes Schuetze

#Scipt takes a number (Km) which represents a distance betwen to nodes. The distance is devided by the speed of light and multiplied by 1000 to get latency.
#NOTE does not account for propagation delay!!!

import sys


distance = float(sys.argv[1])
speed_of_light = 299792458

print distance
result = ((distance*1000)/speed_of_light)*1000

print "%d km take %f ms"%(distance, result)
print result

