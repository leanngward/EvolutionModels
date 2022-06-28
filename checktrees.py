from ete3 import Tree
import os
import re

treefilename  = input("Enter master tree name: ")
dirname = input("Enter tree file directory: ")
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
