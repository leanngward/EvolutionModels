import os
import re
import sys
import json
# pattern search for outfile:

def read_null(filename):
	#set default values
	svdLNL = "NA"
	svdP = "NA"
	tvdLNL = "NA"
	tvdP = "NA"
	tvsLNL = "NA"
	tvsP = "NA"
	sites = "NA"

	#load .json file and create a python dictionary
	with open(filename, 'r+') as file:
		data = json.load(file)

	#single vs double hits
	svdLNL = str(data["test results"]["Double-hit vs single-hit"]["LRT"])
	svdP = str(data["test results"]["Double-hit vs single-hit"]["p-value"])

	#Triple-hit vs double-hit
	tvdLNL = str(data["test results"]["Triple-hit vs double-hit"]["LRT"])
	tvdP = str(data["test results"]["Triple-hit vs double-hit"]["p-value"])

	#Triple-hit vs single-hit
	tvsLNL = str(data["test results"]["Triple-hit vs single-hit"]["LRT"])
	tvsP = str(data["test results"]["Triple-hit vs single-hit"]["LRT"])

	#Site significantly affected by multi n mutations
	sitelist = []
	#interate through the dictionary to find desired output
	for k,v in data.items():
#		print(k)
		if k == "Site substitutions":
			for key,value in v.items():
				realkey = int(key) + 1
				sitelist.append(str(realkey))
	#transform site list in to a comma delmited string
	if len(sitelist) > 1:
		sites = ""
		for i in sitelist:
			sites += i
			sites += ","
		sites = sites[0:-1]

	return svdLNL,svdP,tvdLNL,tvdP,tvsLNL,tvsP,sites; #this is tuple and should be stored as such

#testin = sys.argv[1]
#values = read_null(testin)
#print(values)

#initializes the tuples to store output from function

values = ()

#Value will be set for true if an outfile is found.
nullflag = False
groupname = "NA"

unfinished = []

outputname = sys.argv[2]
outfile = open(outputname,'w+')

#write the headers for outfile
outfile.write("Group\t Single vs. Double LRT \t Single vs. Double p-value \t Triple vs Double LRT \t Triple vs Double p-value \t Triple vs. Single LRT \t Triple vs. Single p-vale \t mnm impacted sites \n")
# Create a section to loop through a directory of group names that are subdirectories.
# Null and Alt out files will be within the subdirectories

filedir = sys.argv[1]

#Loops through every files in the given directory
for file in os.listdir(filedir):
	subdir = os.path.join(filedir,file)
	#Check if the file is subdirectory
	if os.path.isdir(subdir):
		#subdir is the path to the subdirectory WITHOUT THE FILE SLASH
		#Loops through the subdirectory to look for out files
		for subfile in os.listdir(subdir+"/"):
			fullpathsubfile = os.path.join(subdir+"/"+subfile)
			if os.path.isfile(fullpathsubfile):
#				print(subfile)
				if re.search(".treefile",subfile):
					groupname = subfile[4:-23]
				if re.search("FITTER.json",subfile):
					nullflag = True
					nullfile = fullpathsubfile
					values = read_null(nullfile)
#					print(values)
		if nullflag == True:
			outfile.write(groupname+"\t"+values[0]+"\t"+values[1]+"\t"+values[2]+"\t"+values[3]+"\t"+values[4]+"\t"+values[5]+"\t"+values[6]+"\n")
		else:
			outfile.write(groupname+"\t NA \t NA \t NA \t NA \t NA \t NA \t NA \t NA \n")
##		#Done with subdirectory and flagging if there were not outfiles
		if nullflag == False:
			print("No null file for"+subdir)
			unfinished.append(groupname)
		nullflag = False
		groupname = ""
		nullvalues = ()
#OPTIONAL: the feature can be edited to auto run any unrun files
#not used because unrun files either 1. didn't exist or 2. the nodes are working properly with job submission
#name = "undonelist.txt"
#todolist = open(name,"w+")
#for items in unfinishednull:
#	todolist.write("qsub "+items+"_null_runcod.sh \n")
#todolist.close()
outfile.close()
