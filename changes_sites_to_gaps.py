import os
import sys
import Bio
from Bio import SeqIO
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment


#Provide directory of the gene name subdirectories
dirName = sys.argv[1]
dirList = os.listdir(dirName)
geneDirName = ''
geneName = ''


for items in dirList:
	geneDirName = dirName + items
	if(os.path.isdir(geneDirName)):
		geneName = items
		seqFileName = dirName+geneName+"/"+"nuc_"+geneName+"_aligned.phy"
		outFileName = dirName+geneName+"/"+"edited_sites_nuc_"+geneName+"_aligned.phy"
		listName = dirName+geneName+"/"+geneName+"_FITTER_mnm_sites.txt"
		siteList = open(listName,'r')
		sList = []
		for lines in siteList.readlines():
			lines = lines.strip()
			sList.append(lines)
		outFile = open(outFileName,'w')
		#open sequence files to edit
		is_empty = os.path.exists(seqFileName)
		#grab the header line
		infile = open(seqFileName,'r')
		header = infile.readline()
		infile.close()
		outFile.write(header+"\n")
		if is_empty == True:
			align = AlignIO.read(seqFileName,"phylip-relaxed")
			for items in align:
				seq = items.seq
				str_seq = seq
				count = 0
				newseq = ''
				for x in str_seq:
					count += 1
					if str(count) in sList:
						newseq += "-"
#						print(count)
					else:
						newseq += x
				outFile.write(str(items.id)+"  ")
				outFile.write(newseq+"\n")
		outFile.close()
siteList.close()

