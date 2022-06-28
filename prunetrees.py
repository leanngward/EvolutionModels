from ete3 import Tree
import os
import re

#for this code, you'll need to put your .nwk files in their own folder. That is the directory name you will input.  For now, I'll do this by hand.

dirName = input("Please input the directory name: ")
#dirName = "/home/leann/lib/alignments/treefiles/"
#guideTreeName = "/home/leann/lib/alignments/testsuper2.nwk"  #input("Please input file name for supertree: ")
guideTreeName = input("Please input file name for supertree: ")
dirList = os.listdir(dirName)
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
                        for l in range(len(node.name)):            #stores the node the name in the tree of interest w/o the genename
                                if node.name[l]  == "_":
                                        nodename += "_"
                                        break
                                else:
                                        nodename += node.name[l]

                        nodeList.append(nodename)                 #appends the node names to a list
                        nodename = '' 
        #print(nodeList)

        superTree.prune(nodeList)                                 #uses the master tree to prune just the nodes from the treefile
        #print(superTree.get_ascii(attributes=["name", "dist", "label", "complex"]))

        newTreeName = geneName+"_pruned_tree.nwk"                 #create the output file name
        superTree.write(format=0, outfile=newTreeName)            #write the prunces supertree to the newfile
        nodeList = []                                             #empty the node list

        superTree = Tree(guideTreeName)                           #resets the supertree 
