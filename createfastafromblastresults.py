import Bio
import re
from Bio import SeqIO
from Bio import Entrez
from Bio.Seq import Seq

#The output will be named "*gene of interest*_edited.fasta" 


Entrez.email = "leann.g.ward@gmail.com"
fasta = ""

nucids = []

gbfilename = input("Enter genbank file name: ")
gbfile = open(gbfilename, 'r')

genename = input("Enter gene name of interest: ")
outname = genename+".fasta"
out = open(outname, 'w+')
print("Writing output file...")

linelist = []

for items in gbfile.readlines(): #Finds the lines in the genbank file with accession numbers. 
	if items[0:5] == "LOCUS":
		linelist.append(items)

for names in linelist: #finds the location of the XM's and appends them to the nuc id list
    #idnameloc = re.search("XM", names)
    if (re.search("XM", names)):
        idnameloc = re.search("XM",names).start()
        nucids.append(names[idnameloc:idnameloc+13])
    else:
        print("FLAG: " + names + "is not in the proper format.")

###CURATION: This loop will search for any gene locus
gbrecord = ""
geneidlist = []
for ids in nucids:
    handle = Entrez.efetch(db="nuccore",id=ids,rettype="gb",retmode="text")
    for lines in handle.readlines(): 
        gbrecord += lines
    genelocation = re.search("/gene=", gbrecord).end()
    geneidlist.append(gbrecord[genelocation+1:genelocation+13])
    gbrecord = ""

###This searches for repeats in the geneid's
count = 0
seen = set()
unique = []
for locs in geneidlist:
    if locs not in seen:
        unique.append(locs)
        seen.add(locs)
    else:
        print("FLAG: " + locs + " is a duplicate.")
    
for ids in nucids:   
    print("Retrieving...", ids)

    handle = Entrez.efetch(db="nuccore",id=ids,rettype="fasta_cds_na",retmode="text")
    for lines in handle.readlines(): 
        out.write(lines)

out.close()
gbfile.close()


###############################################################
#GET NEW SPECIES NAME
#The follow loop gets the species names for each accession number. 
speciesnamelist = []
for ids in nucids:
    list_name = ""
    speciesname = ""
    handle = Entrez.efetch(db="nuccore",id=ids,rettype="gb",retmode="text")
    for lines in handle.readlines(): 
        list_name+=lines
    
    orgloc = re.search("organism=", list_name).end()
    endloc = re.search("/mol_type", list_name).start()
    speciesname = ""
    for position in range(orgloc+1, endloc):
        speciesname+=list_name[position]
    
    for char in range(len(speciesname)):
        if speciesname[char] == '\"':
            speciesend = char
 
    new_edit = speciesname[0:speciesend]

    for items in range(len(new_edit)):
        if new_edit[items] == " ":
            spaceloc = items
        
    editedname = new_edit[0:spaceloc] + "_" + new_edit[spaceloc+1:]
    speciesnamelist.append(editedname)
newsplist = []  
nn = '' 
for names in speciesnamelist:
    for letters in names:
        if letters != " ":
            nn += letters;
        else:
            nn += "_"
    newsplist.append(nn)
    nn = ''

newin = open(outname, 'r')
newname = genename+"_edited.fasta"
newout = open(newname, "w")
editedfasta = []
count = 0
for lines in newin.readlines():
    if lines[0] == ">":
        newout.write(">")
        newout.write(newsplist[count])
        newout.write("_")
        #newout.write(orthlist[count])
        newout.write(genename)
        newout.write("_")
        newout.write(nucids[count])
        newout.write("\n")
        count += 1
    else:
        newout.write(lines)

newout.close()
newin.close()

