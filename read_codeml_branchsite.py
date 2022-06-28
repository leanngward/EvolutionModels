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

	#Find lnL value
	if re.search("lnL",text):
		lnlpos = re.search("lnL",text).start()
		line = text[lnlpos:lnlpos+55]  #45 is an estimate for the line length. Can be changed.
		if re.search("\):",line):
			colonpos = re.search("\):",line).end()
			pluspos = re.search("\+",line).end()
			lnl = line[colonpos:pluspos-1]
			lnl = lnl.strip()
	else:
		lnl = "NA"

	infile.close()
	return lnl

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
			lnl = lnl.strip()
	else:
		print("alt lnl not found")
		lnl = "NA"

	#Find background omegas
	if re.search("background w",text):
		w = re.search("background w", text).end()
		dline = text[w:w+40]
		dline = dline.strip()
		dline = dline.split()
		bg0 = dline[0]
		bg1 = dline[1]
		bg2a = dline[2]
		bg2b = dline[3]
	else:
		bg0 = 'NA'
		bg1 = 'NA'
		bg2a = 'NA'
		bg2b = 'NA'

	#Find foreground omegas
	if re.search("foreground w",text):
		fw = re.search("foreground w",text).end()
		dline = text[fw:fw+40]
		dline = dline.strip()
		dline = dline.split()
		fg0 = dline[0]
		fg1 = dline[1]
		fg2a = dline[2]
		fg2b = dline[3]
	else:
		fg0 = 'NA'
		fg1 = 'NA'
		fg2a = 'NA'
		fg2b = 'NA'
	#Find BEB Values
	if re.search("Bayes Empirical Bayes",text):
		ps = re.search("Bayes Empirical Bayes",text).end()
		if re.search("The grid",text):
			gr = re.search("The grid", text).start()
			site = text[ps+124:gr-1]
			site = site.strip()
			site = site.split("\n")
			newsite = []
			for item in site:
				item = item+","
				newsite.append(item)
	else:
		site = 'NA'

	infile.close()
	return lnl,bg0,bg1,bg2a,bg2b,fg0,fg1,fg2a,fg2b,newsite;

#initializes the tuples to store output from function
altvalues = ()
sites = ""
#Value will be set for true if an outfile is found.
nullflag = False
altflag = False
groupname = ""

unfinishednull = []
unfinishedalt = []

filedir = sys.argv[1]
outputname = sys.argv[2]
outfile = open(outputname,'w+')


b_name = filedir+"BEB_output.txt"
out2 = open(b_name, 'w+')

#write the headers for outfile
outfile.write("Group\tNull lnL\t\tAlt lnL\tBackground w0\tBackground w1\tBackground w2a\tBackground w2b\tAlt w0\tAlt w1\tAlt w2a\t Alt w2b\n")

out2.write("Group\tBEB Values\n")
# Create a section to loop through a directory of group names that are subdirectories.
# Null and Alt out files will be within the subdirectories

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
				if re.search("_null_branchsite.out",subfile):
					nullflag = True
					nullfile = fullpathsubfile
					nullvalues = read_null(nullfile) 
				if re.search("_alt_branchsite.out",subfile):
					altflag = True
					altfile = fullpathsubfile
					altvalues = read_alt(altfile)
					sites = "\t".join(altvalues[9])
		print(sites)
		if nullflag == True and altflag == True:
			outfile.write(groupname+"\t"+nullvalues+"\t"+altvalues[0]+"\t"+altvalues[1]+"\t"+altvalues[2]+"\t"+altvalues[3]+"\t"+altvalues[4]+"\t"+altvalues[5])
			outfile.write("\t"+altvalues[6]+"\t"+altvalues[7]+"\t"+altvalues[8]+"\n")
			out2.write(groupname+"\t"+sites+"\n")
		elif nullflag == True and altflag == False:
			outfile.write(groupname+"\t"+nullvalues+"\t"+"NA\tNA\tNA\tNA\tNA\tNA\tNA\tNA\tNA\n")
		elif nullflag == False and altflag == True:
			outfile.write(groupname+"\tNA"+altvalues+"\t"+altvalues[1]+"\t"+altvalues[2]+"\t"+altvalues[3]+"\t"+altvalues[4]+"\t"+altvalues[5])
			outfile.write("\t"+altvalues[6]+"\t"+altvalues[7]+"\t"+altvalues[8]+"\n")
			out2.write(groupname+"\t"+sites+"\n")

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
out2.close()
