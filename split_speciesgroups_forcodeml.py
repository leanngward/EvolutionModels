import os
import re
import sys
from Bio import SeqIO


#Directory of orthogroup fasta files - the edited ones
dirName = sys.argv[1]
outDir = sys.argv[2]
#Identify the outgroup species?
outspecies = "dmelanogaster"

recordsdict = {}
grouplist = []
#Loop through the given directory
for file in os.listdir(dirName):
	subdir = os.path.join(dirName,file)
	#Find the subdirectoires - in this case, the orthogroups
	if os.path.isdir(subdir):
		#note: subdir is the path to the subdirectory W/O the file slash
		#Now, loop through the subdirectory for the fasta files
		for subfile in os.listdir(subdir+"/"):
			if (re.search("aligned_protein",subfile)):
					groupname = subfile[16:-3]
					grouplist.append(groupname)
					seqfileName = groupname+".fa"
					seqfilePath = os.path.join(subdir+"/"+seqfileName)
					with open(seqfilePath) as handle:
						for record in SeqIO.parse(handle,"fasta"):
							if re.search("_",record.id):
								underscore = re.search("_",record.id).start()
								speciesname = record.id[0:underscore]
								recordsdict[(groupname,speciesname)] = str(record.seq)

#Now build new files using the recordsdict dictionary
#Goal: For each orthgroup, make two fasta files. each with the outgroup species and one of the species of interest.

spec1 = "banynana"
spec2 = "herato"

outDir1 = os.mkdir(outDir+spec1+"/")
outDir2 = os.mkdir(outDir+spec2+"/")



for group in grouplist:
	outfileName = group+".fa"

	outfile1 = outDir+spec1+"/"+outfileName
	print(outfile1)
	out1 = open(outfile1,'w')
	out1.write(">"+outspecies+"_"+group+"\n")
	record = recordsdict[(groupname,outspecies)]
	out1.write(record+"\n")
	out1.write(">"+spec1+"_"+group+"\n")
	record = recordsdict[(groupname,spec1)]
	out1.write(record+"\n")

	outfile2 = outDir+spec2+"/"+outfileName
	out2 = open(outfile2,'w')
	out2.write(">"+outspecies+"_"+group+"\n")
	record = recordsdict[(groupname,outspecies)]
	out2.write(record+"\n")
	out2.write(">"+spec2+"_"+group+"\n")
	record = recordsdict[(groupname,spec2)]
	out2.write(record+"\n")

	out1.close()
	out2.close()
