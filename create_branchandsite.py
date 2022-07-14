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
        fh.write('model = 2 \n')
        fh.write('NSsites = 2 \n')
        fh.write('Mgene = 0 \n')
        fh.write('fix_kappa = 0 \n')
        fh.write('kappa = 2 \n')
        fh.write('fix_omega = 1 \n')
        fh.write('omega = 1 \n')
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
        fh.write('module load PAML \n')
        fh.write('codeml ')
        fh.write(control_file_name)
        fh.write('\n')

    ## submit the pbs.sh
#    subprocess.call(['qsub', scriptfile_b])



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
        fh.write('model = 2 \n')
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
        fh.write('module load PAML \n')
        fh.write('codeml ')
        fh.write(control_file_name)
        fh.write('\n')

    ## submit the pbs.sh
#    subprocess.call(['qsub', scriptfile_b])


#Provide directory of the gene name subdirectories
dirName = sys.argv[1]

#Provide location of edited tree files
treeDir = sys.argv[2]
flag = ''
mnmFlag = False
#Provide True or False for whether you are tested files with removed sites affected by multi-nucleotide mutations
try:
	flag = sys.argv[3]
	if flag == "T":
		mnmFlag = True
	else:
		mnmFlag = False
except IndexError:
	pass

dirList = os.listdir(dirName)
geneDirName = ''
geneName = ''

for items in dirList:
	geneDirName = dirName + items
	if(os.path.isdir(geneDirName)):
		geneName = items
		treeFileName = treeDir+geneName+"_edited_tree.nwk" #LOCATION OF EDITED TREEFILES
		if mnmFlag == False:
			seqFileName = dirName+geneName+"/"+"nuc_"+geneName+"_aligned.phy"
			nulloutFileName = dirName+geneName+"/"+geneName+"_null_branchsite.out"
			altoutFileName = dirName+geneName+"/"+geneName+"_alt_branchsite.out"
			altScriptName = dirName+geneName+"_alt_bsite_runcod.sh"
			nullScriptName = dirName+geneName+"_null_bsite_runcod.sh"
		else:
			seqFileName = dirName+geneName+"/edited_sites_nuc_"+geneName+"_aligned.phy"
			nulloutFileName = dirName+geneName+"/"+geneName+"_null_mnm_branchsite.out"
			altoutFileName = dirName+geneName+"/"+geneName+"_alt_mnm_branchsite.out"
			altScriptName = dirName+geneName+"_alt_bsite_mnm_runcod.sh"
			nullScriptName = dirName+geneName+"_null_bsite_mnm_runcod.sh"
		codeml_branches_runner(dirName,seqFileName,treeFileName,altoutFileName,altScriptName,geneName)
		null_codeml_branches_runner(dirName,seqFileName,treeFileName,nulloutFileName,nullScriptName,geneName)
