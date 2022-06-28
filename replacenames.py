###This code will take a fasta file as input and replace the full record names with
###shortened versions.

####Example:
####Vanessa_tameamea_atg1_XM_026643934
####Vtamea_atg1

import Bio
import re
from Bio import SeqIO
from Bio import Entrez
from Bio.Seq import Seq


fastaname = input("Please enter the name of the file: ")
genename = input("Please enter the  name of the gene: ")
infile = open(fastaname, 'r')


#this file will contain the full records
outrecname = genename + "_longnames.txt"
outrecord = open(outrecname, 'w')

#header for record text file
outrecord.write("Original Names")
outrecord.write("\n")

#this fasta file with have the shortened names
abbrec = genename + "_final.fasta"
abbrout = open(abbrec, 'w')

namelist = []

spname = ""
sub_str = "_"
occurrence = 2

sequencelist = []

for record in SeqIO.parse(infile, "fasta"):
    outrecord.write(record.id)
    outrecord.write("\t")
    outrecord.write("\n")
    namelist.append(record.id)
    sequencelist.append(record.seq)
    
    
    
shortnames = []
newname = ""  
    
for items in namelist:
    newname += items[0]
    spname = items
    val = -1
    for i in range(0, 1):
        firstpos = spname.find(sub_str, val + 1) 
    
    for i in range(0, occurrence):                #This for loop
        val = spname.find(sub_str, val + 1)       #finds the second underscore, the location is "val"
    newname += items[firstpos+1:val]
    newname += "_"
    newname += genename
    shortnames.append(newname)
    newname = ""
    
for i in range(len(shortnames)):
    abbrout.write(">")
    abbrout.write(shortnames[i].lower())
    abbrout.write("\n")
    abbrout.write(str(sequencelist[i]))
    abbrout.write("\n")



infile.close()
outrecord.close()
abbrout.close()
