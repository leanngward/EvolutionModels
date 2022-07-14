import os
import sys
def absrel_run(prefix,seq_file,treefile,outfile,scriptfile_b,gene_name):
	import subprocess

	with open(scriptfile_b, 'w') as fh:
		fh.write('#!/bin/bash\n')
		fh.write('cd '+prefix+' \n')
		fh.write('/mnt/home/lgw108/.conda/envs/ete3/bin/hyphy absrel --alignment ')
		fh.write(seq_file)
		fh.write(' -tree ')
		fh.write(treefile)
		fh.write(' --branches Foreground ')
		fh.write(' --output ')
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
		nulloutFileName = dirName+geneName+"/"+geneName+"_absrel_model.out"
		nullScriptName = dirName+geneName+"_absrel_model.sh"
		absrel_run(dirName,seqFileName,treeFileName,nulloutFileName,nullScriptName,geneName)
