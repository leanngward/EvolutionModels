import os
import re
import sys

# pattern search for alt file: w (dN/dS) for branches:  0.01893 0.03429
#  			lnL(ntime: 24  np: 27): -20580.011581
# pattern search for null file: omega (dN/dS) =  0.01963
#				lnL(ntime: 24  np: 26): -20583.373058

def read_null(filename):
	infile = open(filename, 'r')
	text = infile.read()
	lnl = "NA"
	dnds = "NA"

	#Find lnL value
	if re.search("lnL",text):
		lnlpos = re.search("lnL",text).start()
		line = text[lnlpos:lnlpos+55]  #45 is an estimate for the line length. Can be changed.
		if re.search("\):",line):
			colonpos = re.search("\):",line).end()
			pluspos = re.search("\+",line).end()
			lnl = line[colonpos:pluspos-1]
	else:
		lnl = "NA"
	#Find dN/dS values
	if re.search("omega \(dN\/dS\) = ", text):
		omega = re.search("omega \(dN\/dS\) = ", text).end()
		dline = text[omega:omega+10]
		dnds = dline.strip()
	else:
		dnds = "NA"
	infile.close()
	return lnl,dnds; #this is tuple and should be stored as such

def read_alt(filename):
	infile = open(filename, 'r')
	text = infile.read()
	lnl = "NA"
	dnds0 = "NA"
	dnds1 = "NA"

	#Find lnL value
	if re.search("lnL",text):
		lnlpos = re.search("lnL",text).start()
		line = text[lnlpos:lnlpos+55]
		if re.search("\):",line):
			colonpos = re.search("\):",line).end()
			pluspos = re.search("\+",line).end()
			lnl = line[colonpos:pluspos-1]
	else:
		print("alt lnl not found")
		lnl = "NA"
	#Find dN/dS values
	if re.search("w \(dN\/dS\) for branches:", text):
		w = re.search("w \(dN\/dS\) for branches:  ", text).end()
		dline = text[w:w+25]
		if re.search("\d\s\d",dline):
			middle = re.search("\d\s\d",dline).start()
			dnds0 = dline[:middle+1]
			dnds1 = dline[middle+1:middle+10]
			dnds0 = dnds0.strip()
			dnds1 = dnds1.strip()
	else:
		print("all dnds values not found")
		dnds0 = "NA"
		dnds1 = "NA"
	infile.close()
	return lnl,dnds0,dnds1;

#initializes the tuples to store output from function
nullvalues = ()
altvalues = ()

#Value will be set for true if an outfile is found.
nullflag = False
altflag = False
groupname = ""

unfinishednull = []
unfinishedalt = []

outputname = sys.argv[2]
outfile = open(outputname,'w+')

#write the headers for outfile
outfile.write("Group\tNull lnL\tNull dN/dS\tAlt lnL\tAlt Omega 0 Background\tAlt Omega 1\n")
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
				if re.search("_null_branch.out",subfile):
					nullflag = True
					nullfile = fullpathsubfile
					nullvalues = read_null(nullfile) 
				if re.search("_alt_branch.out",subfile):
					altflag = True
					altfile = fullpathsubfile
					altvalues = read_alt(altfile)
		if nullflag == True and altflag == True:
			outfile.write(groupname+"\t"+nullvalues[0]+"\t"+nullvalues[1]+"\t"+altvalues[0]+"\t"+altvalues[1]+"\t"+altvalues[2]+"\n")
		elif nullflag == True and altflag == False:
			outfile.write(groupname+"\t"+nullvalues[0]+"\t"+nullvalues[1]+"\t"+"NA\tNA\tNA\n")
		elif nullflag == False and altflag == True:
			outfile.write(groupname+"\tNA\tNA\t"+altvalues[0]+"\t"+altvalues[1]+"\t"+altvalues[2]+"\n")

		#Done with subdirectory and flagging if there were not outfiles
		if nullflag == False:
			print("No null file for"+subdir)
			unfinishednull.append(groupname)
		if altflag == False:
			print("No alt file for"+subdir)
			unfinishedalt.append(groupname)
		nullflag = False
		altflag = False
		groupname = ""
		altvalues = ()
		nullvalues = ()

name = "undonelist.txt"
todolist = open(name,"w+")
for items in unfinishednull:
	todolist.write("qsub "+items+"_null_runcod.sh \n")
for items in unfinishedalt:
	todolist.write("qsub "+items+"_alt_runcod.sh \n")

todolist.close()
outfile.close()
