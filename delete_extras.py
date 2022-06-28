import os
import sys

#Provide the full path for directory of gene groups subdirectories that have the files you want to delete
mainDir = sys.argv[1]

#Provide the string flag for the file you want to delete
flag = sys.argv[2]

#Loop through the main directory
for subdirs in os.listdir(mainDir):
	#make full path for subdirs
	d = os.path.join(mainDir,subdirs)
	#check if the path is a subdirectory
	if os.path.isdir(d):
		#Loop through the files in the subdirectories
		for subdirs in os.listdir(d):
			#When you find the file you don't want, remove it
			if flag in subdirs:
				os.remove(d+"/"+subdirs)
