#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze

#Script adds interfaces to .dot files

import sys

def read_in():
	lines = sys.stdin.readlines()
	for i in range(len(lines)):
		lines[i] = lines[i].replace('\n','')
	#print lines
	return lines

output = ""
data = read_in()
for line in data:
	#print "HELLO"
	output = "\t" + line + "\t[label=1,headlabel=\"%s-%s\" ,alias = 1,throughput=16,latency=4,delay=3,bandwidth = 10];"%(str(line[7:]),str(line[:3]))
	print output
sys.stdout.flush()



