import os
import re

dirName = input("Please enter pruned tree directory path: ")
#dirName = "/home/leann/lib/alignments/prunedtrees/"
dirList = os.listdir(dirName)

#This scripts takes treefiles created by prunetrees.py and parses them by adding the genename after underscores
#and changing the "2" to a "$1" to run with codeml.
#It outputs all the treefiles as *genename*_edited_tree.nwk

newline = ''

for filename in dirList:
        endloc = re.search("_", filename).end()
        geneName = filename[0:endloc-1]
        newFileName = geneName + "_edited_tree.nwk"
        openFileName = dirName + filename
        file = open(openFileName, 'r')
        for c in file.readline():
                if c == "2":
                        newline += "$1"
                elif c == "_":
                        newline += "_"
                        newline += geneName
                else:
                        newline += c

#       print(newline)
        newFileName = geneName + "_edited_tree.nwk"
        outfile = open(newFileName, 'w')
        outfile.write(newline)



        outfile.close()
        file.close()
        newline = ''
