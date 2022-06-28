from ete3 import Tree
import os
import re
import sys
import shutil


#For this code, you'll need a directory of .nwk tree files in their own folder. That is the directory name you will input.
#Then for each file that directory, they will be edited and the new edited file will be placed in an output directory.

dirName = sys.argv[1]
dirList = os.listdir(dirName)
outputDirName = sys.argv[2]
outputDir = os.makedirs(outputDirName)
#for file in dirList:
#	srcpath = dirName+file
#	despath = outputDirName + file
#	if os.path.isfile(srcpath):
#		shutil.copy(srcpath,despath)
#		print('copied',file)

#guideTreeName will be the name of your master tree
guideTreeName = sys.argv[3]
superTree = Tree(guideTreeName)

#treeFile -> the gene tree
	#NAME FORMAT: treefile name must begin with "*genename*_"
#superTree -> the master tree
	#FORMATTING: Node names in the tree must be: *speciesname*_
                    #Genes or species of interest should be followed by a ":2"
#newTree -> tree produced by the program

findNodeList = []
nodeList = []
newline = ''
nodename = '' 

for filename in dirList:
	print("Looking at..."+filename+"\n")
	treeFile = Tree(dirName+filename)                          #creates the full path for the treefile
	endloc = re.search("_", filename).end()                    #finds the position of underscore
	geneName = filename[0:endloc-1]                            #uses underscore position to find the genename

	for node in treeFile.traverse("levelorder"):               #traverses the tree of interest
		if node.name:                                     
			for l in range(len(node.name)):            #stores the node name in the tree of interest w/o the genename
				if node.name[l]  == "_":
					nodename += "_"
					break
				else:
					nodename += node.name[l]

			nodeList.append(nodename)                 #appends the node names to a list
			nodename = '' 

	superTree.prune(nodeList)                                 #uses the master tree to prune just the nodes from the treefile
	#print(superTree.get_ascii(attributes=["name", "dist", "label", "complex"]))
	
	newTreeName = outputDirName+geneName+"_pruned_tree.nwk"                 #create the output file name and put into output directory
	superTree.write(format=0, outfile=newTreeName)		  #write the prunces supertree to the newfile
	nodeList = []                                             #empty the node list

	superTree = Tree(guideTreeName)                           #resets the supertree 
