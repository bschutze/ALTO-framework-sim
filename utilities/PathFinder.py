#!/usr/bin/python

#Master-Thesis dot parsing framework (PING MODULE)
#Date: 23.09.2014
#Author: Bruno-Johannes Schuetze
#uses python 2.7.6

#starts findpath.pl untill results are found, then stores the results in a .txt

import pexpect, time
import sys

print "\nStarting the Pathfinder, wish me Luck!"

path0 = "TEST_SANITY_CORE_GEODETIC_GER.dot"
path1 = "CORE_GEODETIC_GER.dot"
#path2 = "CORE_GEODETIC_USA.dot"
#path3 ="AS4_Network"

print ("./gen_Interfaces.py "+path0+" | findpath.pl")

cond = True
counter = 0

fout = open("PATHFINDER_RES_SANITY_local.txt", "w")

fout.write ('############# %4d.%02d.%02d   %02d:%02d:%02d \n' % time.localtime()[:-3])

child = pexpect.spawn("bash")
child.logfile = fout


while (cond):
	fout.write ('############# %4d.%02d.%02d   %02d:%02d:%02d \n' % time.localtime()[:-3])
	print "Searching. Round #: ", counter
	counter+= 1
	child.sendline('./gen_Interfaces.py '+path0+' | ./findpath.pl')
	#child.sendline('cat AS4_Network\ \|\ findpath.pl')
	res = child.expect(['could not find solutions.','JOHANNES_MODIFIED'], timeout=None)
	print res
	if (res==0):
		continue
	else:
		cond = False
		#sleep(10)
		#f = open("PATHFINDER_RES.txt", "w")
		#f.write(child.before)
		#f.close()

fout.write ('# %4d.%02d.%02d   %02d:%02d:%02d \n' % time.localtime()[:-3])

fout.close()

print "Pathfinder was sucessfull!!!! Open the Champagne!!"
