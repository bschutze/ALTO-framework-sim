#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 14.01.2014
#Author: Bruno-Johannes Schuetze

#Script adds interfaces to .dot files
# usually executed like:
#> cat file.txt | add_Interfaces.py
# file.txt example:
#\t123 -> 321


import sys

def read_in():
	lines = sys.stdin.readlines()
	for i in range(len(lines)):
		lines[i] = lines[i].replace('\n','')
	#print lines
	return lines

output = ""


try:
	file_handle = open('Conf/networkGen_config.txt', 'r')
except (OSError, IOError) as e:
	print e
	print "Goodbye"


data = read_in()
for line in data:
	#print "HELLO"
	#if its not a edge but a city name
	if '//' in line:
		output = "\t" + line
		print output
	#if there is a empty line
	elif len(line) < 3:
		continue
	#esle its a edge and meta needs to be added
	else:
		output = "\t" + line + "\t[label=1,headlabel=\"%s-%s\" ,alias = 1,throughput=16,latency=4,delay=3,bandwidth = 10];"%(str(line[7:]),str(line[:3]))
		print output
sys.stdout.flush()


