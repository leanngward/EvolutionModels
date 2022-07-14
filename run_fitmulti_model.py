import os
import sys
def fitmodel_run(prefix,seq_file,treefile,outfile,scriptfile_b,gene_name):
	import subprocess

	with open(scriptfile_b, 'w') as fh:
		fh.write('#!/bin/bash\n')
		fh.write('cd '+prefix+' \n')
		fh.write('/mnt/home/lgw108/.conda/envs/ete3/bin/hyphy /mnt/home/lgw108/.conda/envs/ete3/lib/hyphy/TemplateBatchFiles/SelectionAnalyses/FitMultiModel.bf --alignment ')
		fh.write(seq_file)
		fh.write(' -tree ')
		fh.write(treefile)
		fh.write('> ')
		fh.write(outfile)
		fh.write('\n')

    ## submit the pbs.sh
#	subprocess.call(['qsub', scriptfile_b])


#Provide directory of the gene name subdirectories
dirName = sys.argv[1]

#Provide location of edited tree files
treeDir = sys.argv[2]


dirList = os.listdir(dirName)
geneDirName = ''
geneName = ''


for items in dirList:
	geneDirName = dirName + items
	if(os.path.isdir(geneDirName)):
		geneName = items
		seqFileName = dirName+geneName+"/"+"nuc_"+geneName+"_aligned.fasta"
		treeFileName = treeDir+geneName+"_edited_tree.nwk" #LOCATION OF EDITED TREEFILES
		nulloutFileName = dirName+geneName+"/"+geneName+"_fitmodel.out"
		nullScriptName = dirName+geneName+"_fitmodel.sh"
		fitmodel_run(dirName,seqFileName,treeFileName,nulloutFileName,nullScriptName,geneName)
