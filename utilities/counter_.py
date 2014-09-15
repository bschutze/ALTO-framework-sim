#!/usr/bin/python

import os

def genStats():
	search_str = "->"
	counter = 0
	nodeCount = 0
	directory = "Output/DOT/"
	output_str =""
	for fname in sorted(os.listdir(directory)):
		if fname.endswith(".dot") and not "NETWORKMAP" in fname:
			with open(directory + fname, "w+") as f:
				for line in f:
					if search_str in line:
						counter = counter +1
				output_str = "\nFile: " + fname + "\nEdge Count: " + str(counter)+"\nNode Count: "+str(nodeCount)+"\n"
			with open("Output/TOTAL_STATS_COUNT.txt", "a") as newFile:
				newFile.write(output_str + "\n*******************************\n")
		counter=0
