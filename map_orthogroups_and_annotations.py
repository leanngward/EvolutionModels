import os
import re
import sys
from Bio import SeqIO

#Give directory with orthogroup fasta files (from OrthoFinder results)
dirName = sys.argv[1]

#Give the annotation files map of interest (.gff.CDS / .gtf.CDS) made from a previous script
mapName = sys.argv[2]
inMap = open(mapName,'r')
mapDict = {}
for line in inMap.readlines():
	if line[0] != "#":
		lines = line.split("\t")
		protein = lines[2]
		mapDict[protein] = line



inMap.close()

#Give the output file name?
outName = sys.argv[3]
outFile = open(outName,'w')
outFile.write("#Orthogroup\tgeneid\ttx_id\tcds_id\tchomname\tpos\tframes\n")
count = 0
for ogfile in os.listdir(dirName):
	orthoname = ogfile[:-3]

	inFile = dirName+ogfile
	with open(inFile) as handle:
		for record in SeqIO.parse(handle, "fasta"):
			for key,value in mapDict.items():
				if re.search(key,str(record.id)):
					count += 1
					outFile.write(orthoname+"\t")
					outFile.write(value)
					#outFile.write("\n")
#outFile.close()
