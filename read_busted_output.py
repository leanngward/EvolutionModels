import os
import re
import sys
import json
# pattern search for outfile:

def read_null(filename):
	#set default values
	LRT = "NA"
	pvalue = "NA"
	constrainedLNL = "NA"
	mg94LNL = "NA"
	ngtrLNL = "NA"
	unconstrainedLNL = "NA"

	#load .json file and create a python dictionary
	with open(filename, 'r+') as file:
		data = json.load(file)
	#interate through the dictionary to find desired output
#	for k,v in data.items():
		#print(k)
		#"test results" should contain two items. 'LRT':#####, 'p-value':#######
		#testresultsdict = data["test results"]
		#LRT = testresultsdict["LRT"]
		#pvalue = testresultsdict["p-value"]
	LRT = str(data["test results"]["LRT"])
	pvalue = str(data["test results"]["p-value"])
		#"fits" to access the models
			#get the log likelihood value for each model that was run
	constrainedLNL = str(data["fits"]["Constrained model"]["Log Likelihood"])
	mg94LNL = str(data["fits"]["MG94xREV with separate rates for branch sets"]["Log Likelihood"])
	ngtrLNL = str(data["fits"]["Nucleotide GTR"]["Log Likelihood"])
	unconstrainedLNL = str(data["fits"]["Unconstrained model"]["Log Likelihood"])


	return LRT,pvalue,constrainedLNL,mg94LNL,ngtrLNL,unconstrainedLNL; #this is tuple and should be stored as such

#testin = sys.argv[1]
#values = read_null(testin)
#print(values)

#initializes the tuples to store output from function

values = ()

#Value will be set for true if an outfile is found.
nullflag = False
groupname = ""

unfinished = []

outputname = sys.argv[2]
outfile = open(outputname,'w+')

#write the headers for outfile
outfile.write("Group\t LRT \t p-value \t Constrained model \t MG94xREV \t NucleotideGTF \t Unconstrained model \n")
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
				if re.search(".treefile",subfile):
					groupname = subfile[4:-23]
				if re.search("BUSTED.json",subfile):
					nullflag = True
					nullfile = fullpathsubfile
					values = read_null(nullfile)
		if nullflag == True:
			outfile.write(groupname+"\t"+values[0]+"\t"+values[1]+"\t"+values[2]+"\t"+values[3]+"\t"+values[4]+"\t"+values[5]+"\n")
		else:
			outfile.write(groupname+"\t NA \t NA \t NA \t NA \t NA \t NA \t NA \n")
#		#Done with subdirectory and flagging if there were not outfiles
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
