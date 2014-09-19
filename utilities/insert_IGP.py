#!/usr/bin/python
#Master-Thesis dot parsing framework
#Date: 17.09.2014
#Author: Bruno-Johannes Schuetze

import sys

def read_in():
	lines = sys.stdin.readlines()
	for i in range(len(lines)):
		lines[i] = lines[i].replace('\n','')
	#print lines
	return lines
	
path = str(sys.argv[1])
file_handle = open (path, "r")


output = ""
igp_weight = ""
data = read_in()
for line in data:
	#print line
	pos = line.find("//")
	if pos > 0:
		print "we have a // at pos ", pos
	else:		
		pos = line[1:].find("\t[")
		output = line[1:pos+1]	
		print output
		for line2 in file_handle.readlines():
			
			print "The output: ",output
			print line2
			tmp = line2.find(output)
			print tmp
			#print tmp
			if tmp >= 0 :
			 	start = line2.find(" =  ")
			 	end = line2.find(" #")
			 	igp_weight = line2[start+4:end]
			 	print "%s[label=%s]"%(output,igp_weight)
		#print igp_weight
		pos = line.find("[")
		pos2 = line.find("headlabel")
		tmp = line[pos:]
		file_handle.seek(0)
		#output = line[:pos] + 
		#print output
		#output = "\t" + line + "\t[label=1,headlabel=\"%s-%s\" ,alias = 1,throughput=16,latency=4,delay=3,bandwidth = 10];"%(str(line[7:]),str(line[:3]))
		#print output
		
sys.stdout.flush()


#for line in f.readlines():
