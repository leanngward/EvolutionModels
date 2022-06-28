### This part of the code should FLAG any duplicate species names in the protein sequences to be removed.
import Bio
import re
from Bio import SeqIO
from Bio.Seq import Seq

ifilename = input("Please enter the file you want to curate: ")
#genename = input("Please enter the genename for this file.: ")
ifile = open(ifilename, 'r')

namelist = []
uniq = []
seen = set()
spname = ""
sub_str = "_"
occurrence = 2



for record in SeqIO.parse(ifile, "fasta"):
    spname = record.id
    val = -1
    for i in range(0, occurrence):                #This for loop
        val = spname.find(sub_str, val + 1)       #finds the second underscore, the location is "val"
    
    spname = spname[0:val].lower()
    namelist.append(spname)

for items in namelist:                                #This for loop flags any repeat species names
    if items not in seen:
        uniq.append(items)
        seen.add(items)
    else:
        print("FLAG: " + items + " is a duplicate.")


ifile.close()
