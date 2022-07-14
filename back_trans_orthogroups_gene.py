import os
import sys
import re
from Bio import SeqIO
#run command: python3 rename_orthogroup_genes.py *species genome files directory* *orthogroup files directory* *new directory name*


names = {}
seqs = {}
#Build a dictionary with the key as the record id and the species as the value
species = sys.argv[1]
for spec in os.listdir(species):
	speciesname = spec[:-3]
#	names.setdefault(speciesname, [])  #Initializes a list of values for a key that is not defined yet
	f = os.path.join(species, spec)    # joins directory location with filename
	# checking if it is a file
	if os.path.isfile(f):
		with open(f) as handle:
			for record in SeqIO.parse(handle, "fasta"):
				names[record.id] = speciesname       #save the record.id into a list for its respective species
				seqs[record.id] = record.seq

#Loop through a directory of your orthogroup files
directory = sys.argv[2]
#Create a directory for edited orthogroup files to be written to
new_dir = sys.argv[3]
os.mkdir(new_dir)

for og in os.listdir(directory):
	#Create a sub directory for each orthogroup
	orthoname = og[:-3]
#	sub_dir = new_dir+orthoname+"/"
#	os.mkdir(sub_dir)
	#adds directory path to the orthogroup file name for opening
	f = os.path.join(directory, og) 
	#open a new file in the new directory
	newfile = open(new_dir+og, "w+")
	#checking if it is a file
	if os.path.isfile(f):
		with open(f) as handle:
			#loops through the sequence within each fasta file individually
			for record in SeqIO.parse(handle, "fasta"):
				species = names[record.id]
				seq = seqs[record.id]
				#write new record id
				newfile.write(">"+str(record.id)+"\n")
				#write sequence
				newfile.write(str(seq)+"\n")
	newfile.close()
