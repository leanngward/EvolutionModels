from ete3 import Tree
import os
import re
import sys

#run command: python3 check_trees1.py [master tree] [directory of tree files you are checking]
#USE: check spelling of species names by cross referencing with master tree. helps make sure both are correct

treefilename  = sys.argv[1]
dirname = sys.argv[2]
supertree = Tree(treefilename)
exists = False
checkname = ''
newcheckname = ''

mastertreenamelist = []
for node in supertree.traverse("postorder"):
	mastertreenamelist.append(node.name)


dirlist = os.listdir(dirname)
for filename in dirlist: 
	currenttree = Tree(dirname+filename)
	for node in currenttree.traverse("postorder"):
		#extracts species name from node
		for l in range(len(node.name)):
			if node.name[l] == "_":
				newcheckname += "_"
				break
			else:
				newcheckname += node.name[l]
		
		#finds species in mastertree
		if (newcheckname in mastertreenamelist):
			exists = True
		else:
			print("Possible mistake for "+node.name+" in "+filename)
		
		newcheckname = ''
