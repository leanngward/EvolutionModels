#Combine multiple fasta fasta file

genename = input("What is the name of the gene for this file?: ")
numfiles = input("How many files do you want to combine? Enter: ")
numfiles = int(numfiles)

count = 0
sequence = []
content = ""
while count < numfiles:
    strcount = str(count+1)
    filename = input("Please enter file name " + strcount + ": ")
    newfile = open(filename, "r")
    for lines in newfile.readlines():
        content += lines
    sequence.append(content)
    content = ""
    count += 1

outname = genename + "_combined.fasta"
outfile = open(outname, "w")
for items in sequence:
    outfile.write(items)
    outfile.write("\n")




newfile.close()
outfile.close()
