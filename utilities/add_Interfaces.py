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

altoCount = 0#will be increased at every city, to roughly group citys into one PID
data = read_in()
for line in data:
	#print "HELLO"
	#if its not a edge but a city name
	if '//' in line:
		altoCount +=1 #increase by one once new City is worked with.
		output = "\t" + line
		print output
	#if there is a empty line
	elif len(line) < 3:
		continue
	#else its a edge and meta needs to be added
	else:
		igp_pos = line.find("=")
		output = "\t" + line[:igp_pos] + "\t[label=%s,headlabel=\"%s-%s\" ,alias=1,latency=4];"%(str(line[igp_pos+1:]),str(line[7:igp_pos]),str(line[:3]))
		print output
sys.stdout.flush()


