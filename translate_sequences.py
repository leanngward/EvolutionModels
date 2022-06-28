#Translate NUC sequence to proteins
#Check the for stop codons and remove them. 

from Bio import SeqIO
from Bio.Seq import Seq
import sys
import os

codon_stop_array = ["TAG", "TGA", "TAA", "UGA", "UAA", "UAG"]


#Provide the name of a directory filled with  gene group directories. Assumes there is one file in each group.
#Script should translate that nucleotide files as well as remove stop codons.

maindirectory = sys.argv[1]
#Loops through given directory
for subdir in os.listdir(maindirectory):
	for file in os.listdir(maindirectory+subdir+"/"):
		f = os.path.join(maindirectory+subdir,file)
		if os.path.isfile(f):
			#Writes the output file
			proteinfile_name = "protein_"+file
			proteinfile = open(maindirectory+subdir+"/"+proteinfile_name,"w+")
			with open(f) as handle:
				for record in SeqIO.parse(handle, "fasta"): #This for loop removes unwanted stop codons and translates the amino acids.
					tempRecordSeq = list(record.seq)
					for index in range(0, len(record.seq), 3):
						codon = record.seq[index:index+3]
						if codon in codon_stop_array:
							tempRecordSeq[index:index+3] = '?','?','?'
						record.seq = Seq("".join(tempRecordSeq))
			with open(f) as handle:
				for record in SeqIO.parse(handle, "fasta"):
					proteinfile.write(">")
					proteinfile.write(record.id)
					proteinfile.write("\n")
					translatedrec = record.seq.translate(to_stop=True)
					proteinfile.write(str(translatedrec))
					proteinfile.write("\n")
    
    
			proteinfile.close()

#https://www.biostars.org/p/296261/

