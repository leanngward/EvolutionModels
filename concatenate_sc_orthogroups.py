import os
import sys


#Provide name for the an outer directory filled with subdirectories (named as the gene group names)
dirName = sys.argv[1]
outName = sys.argv[2]
dirList = os.listdir(dirName)
geneDirName = ''
geneName = ''

outFile = open(outName,'w')
for items in dirList:
	geneDirName = dirName + items
	if(os.path.isdir(geneDirName)):
		geneName = items
		groupFileName = dirName+geneName+"/"+geneName+".fa"
		infile = open(groupFileName,'r')
		for lines in infile.readlines():
			outFile.write(lines)
		infile.close()

outFile.close()
