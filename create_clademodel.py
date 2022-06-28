import os
import sys
def null_codeml_branches_runner(codeml_prefix,seq_file,treefile,outfile,scriptfile_b,gene_name):
    import subprocess
    #create the control file for codeml to run
    control_file_name = codeml_prefix  + gene_name + '_null.ctl'
    with open(control_file_name, 'w') as fh:
        fh.write('seqfile = ' + seq_file +'\n')
        fh.write('treefile = '+ treefile +'\n')
        fh.write('outfile = ' + outfile +'\n')
        fh.write('noisy = 9 \n')
        fh.write('verbose = 0 \n')
        fh.write('runmode = 0 \n')
        fh.write('seqtype = 1 \n')
        fh.write('CodonFreq = 2 \n')
        fh.write('clock = 0 \n')
        fh.write('aaDist = 0 \n')
        fh.write('model = 0 \n')
        fh.write('NSsites = 0 \n')
        fh.write('Mgene = 0 \n')
        fh.write('fix_kappa = 0 \n')
        fh.write('kappa = 2 \n')
        fh.write('fix_omega = 0 \n')
        fh.write('omega = 0.4 \n')
        fh.write('fix_alpha = 1 \n')
        fh.write('alpha = 0 \n')
        fh.write('Malpha = 0 \n')
        fh.write('ncatG = 8  \n')
        fh.write('getSE = 0 \n')
        fh.write('RateAncestor = 1 \n')
        fh.write('Small_Diff = .5e-6 \n')
        fh.write('method = 0 \n')

    with open(scriptfile_b, 'w') as fh:
        fh.write('#!/bin/bash\n')
        fh.write('cd '+codeml_prefix+' \n')
        fh.write('/home/amanda/software/paml4.9j/bin/codeml ')
        fh.write(control_file_name)
        fh.write('\n')

    ## submit the pbs.sh
    subprocess.call(['qsub', scriptfile_b])



def codeml_branches_runner(codeml_prefix,seq_file,treefile,outfile,scriptfile_b, gene_name):
    import subprocess
    #create the control file for codeml to run
    control_file_name = codeml_prefix  + gene_name + '_alt.ctl'
    with open(control_file_name, 'w') as fh: 
        fh.write('seqfile = ' + seq_file +'\n')
        fh.write('treefile = '+ treefile +'\n')
        fh.write('outfile = ' + outfile +'\n')
        fh.write('noisy = 9 \n')
        fh.write('verbose = 0 \n')
        fh.write('runmode = 0 \n')
        fh.write('seqtype = 1 \n')
        fh.write('CodonFreq = 2 \n')
        fh.write('clock = 0 \n')
        fh.write('aaDist = 0 \n')
        fh.write('model = 3 \n')
        fh.write('NSsites = 2 \n')
        fh.write('Mgene = 0 \n')
        fh.write('fix_kappa = 0 \n')
        fh.write('kappa = 2 \n')
        fh.write('fix_omega = 0 \n')
        fh.write('omega = 0.4 \n')
        fh.write('fix_alpha = 1 \n')
        fh.write('alpha = 0 \n')
        fh.write('Malpha = 0 \n')
        fh.write('ncatG = 8  \n')
        fh.write('getSE = 0 \n')
        fh.write('RateAncestor = 1 \n')
        fh.write('Small_Diff = .5e-6 \n')
        fh.write('method = 0 \n')

    with open(scriptfile_b, 'w') as fh:
        fh.write('#!/bin/bash\n')
        fh.write('cd '+codeml_prefix+' \n')
        fh.write('/home/amanda/software/paml4.9j/bin/codeml ')
        fh.write(control_file_name)
        fh.write('\n')

    ## submit the pbs.sh
    subprocess.call(['qsub', scriptfile_b])


#Provide directory of the gene name subdirectories
dirName = sys.argv[1]

#Provide location of edited tree files
treeDir = sys.argv[2]

#nullInFile = "/home/leann/lib/longevity_dnds/null.ctl"
#altInFile = "/home/leann/lib/longevity_dnds/alternative.ctl"
#nullInFile = input("Input Blank Null file name: ")
#altInFile = input("Input Blank Alt file name: ")

dirList = os.listdir(dirName)
geneDirName = ''
geneName = ''


for items in dirList:
	geneDirName = dirName + items
	if(os.path.isdir(geneDirName)):
		geneName = items
		seqFileName = dirName+geneName+"/"+"nuc_"+geneName+"_aligned.phy"
		treeFileName = treeDir+geneName+"_edited_tree.nwk" #LOCATION OF EDITED TREEFILES
		nulloutFileName = dirName+geneName+"/"+geneName+"_null_clade.out"
		altoutFileName = dirName+geneName+"/"+geneName+"_alt_clade.out"
		altScriptName = dirName+geneName+"_alt_clade_runcod.sh"
		nullScriptName = dirName+geneName+"_null_clade_runcod.sh"
		codeml_branches_runner(dirName,seqFileName,treeFileName,altoutFileName,altScriptName,geneName)
		null_codeml_branches_runner(dirName,seqFileName,treeFileName,nulloutFileName,nullScriptName,geneName)
