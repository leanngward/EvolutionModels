import os
import re
import sys

#Provide a directory a pruned tree files
dirName = sys.argv[1]
dirList = os.listdir(dirName)

outName = sys.argv[2]
outDir = os.mkdir(outName)
#This scripts takes treefiles created by prunetrees.py and parses them by adding the genename after underscores
#and changing the "2" to a {Foreground} for HyPhy models allowng a predefined hypothesis
#It outputs all the treefiles as *genename*_edited_tree.nwk into the provided output directory name.

newline = ''

for filename in dirList:
	endloc = re.search("_", filename).end()
	geneName = filename[0:endloc-1]
	openFileName = dirName + filename
	file = open(openFileName, 'r')
	for c in file.readline():
		if c == ":":
			pass
		elif c == "1":
			pass
		elif c == "2":
			newline += "{Foreground}"
		elif c == "_":
			newline += "_"
			newline += geneName
		else:
			newline += c

	newFileName = outName + geneName + "_edited_tree.nwk"
	outfile = open(newFileName, 'w')
	outfile.write(newline)



	outfile.close()
	file.close()
	newline = ''
