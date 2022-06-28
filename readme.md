##### This file will explain what the butterfly pipeline files do. 
##### They are listed in the order to be used.


## createfastafromblastresults.py

This file takes a genbank file as input (gotten from blastn). It will create two files. <br>
*genename*.fasta and *genename*_edited.fasta. The first one is just a fasta with all the sequences in the genbank file. <br>
The second contains names edited in the format "Species Name _ GeneName _ Accession Number."

Output File Name: *genename*.fasta and *genename*_edited.fasta

This code also flags two situations:
1. If the Accession number in the genbank is not in the traditional XM format, then it is flagged and not added added to the fasta automatically. 
		Note: The non-XM format genes can be gotten from NCBI. Retrieve the CDS sequence from the website. 
2. If any of the gene id's are repeated, then they are flagged. One of them should be removed. 

## combinefastas.py

Input File Name: *genename*_edited.fasta
This code puts together as many fasta files as you choose. For the purpose of this pipeline, <br>
it is being used to combine the genes from ensembl, lepbase, and ncbi.

## findduplicates.py

Input: *genename*_combined.fasta [or any fasta file!]

This file will flag if there are any duplicate species in your fasta file. Make sure to remove any duplicates before using replacenames.py or aligning the sequences. 

No output.

## replacenames.py

Input:*genename*_combined.fasta

Output: *genename*_final.fasta AND *genename*_longnames.fasta

This code creates two new files. One has a stored listed of the names of the genes in the inputted fasta file. 
The second file is a new fasta that, for each gene, stores the species name and adds the user inputted gene name. 
	Note: For the pipline later on, it is reccommended that the genename be given in lowercase letters. 

## translate_sequences.py
Input File Name: *genename*_final.fasta

This code translates the final fasta from nucleotides into proteins for the alignment. 
The output file is named with this convention "protein _ *genename* _ final.fasta" 

Output: protein _ *genename* _ final.fasta

## autotest.sh (RENAME when finished)

This code loops through a directory containing more directories, each named with the gene. 
	NOTE: Keep the folder names all lowercase. 
For each gene folder,
	It finds the "protein_*genename*_final.fasta" and aligns it in MAFFT.
		MAFFT OUTPUT: "aligned_protein_*genename*_final.fasta
	It backtranslates the alignment with Pal2Nal using the protein file above and the *genename*_final.fasta file.
		PAL2NAL OUTPUT: nuc_*genename*_aligned.fasta
	It runs iqtree on the nucleotide alignment above.
	It takes the nucleotide alignment and runs fasta2phylipFullName.py on the nucleotide alignment.
		PHYLIP OUTPUT: "nuc_*genename*_aligned.phy"
		
		
		
## prunetrees.py
	
	Must activate ete3 conda environment to use this script.
	INPUT: name of tree files directory. Copied from the .treefiles from the autotest.sh run. 
	Code requires a master tree with all the species in the gene trees. 
		- The original master tree is labelled with '2' on the branches of interest.
	For every tree in the gene tree,
		Prunes the master tree down to the species in that gene tree.
		Replaces the 2's with $1 in order to run with codeml.
	OUTPUT: *genename*_pruned_tree.nwk
	
## parsetree.py
	INPUT: name of prunedtree.py output
	This python code edits the '2' in the tree to $1 in order to be run with codeml. 
	OUTPUT: *genename*_edited_tree.nwk (these will be put into editedtreefiles folder)



Next, codeml needs to be run on trees in two different ways: a single omega for <br>
all branches or two omegas (w1 for background branches and w2 for heliconius branches). 


## checktrees.py

        Code double checks for spelling errors, etc., by seeing if all the species in the treefiles
        exist in the mastertree. 
	
## createcod.py
	
	This software creates the control files to run codeml and submits them to the qsub to run.
        INPUT:
        1.  Needs to be told the directory that genes are in. The directory should be made up
        of subdirectories named as the gene and containing the necessary files.
        2.  Need to be told the directory of where the edited codeml trees are. Must be changed within the script.
        3.  Whether the null or alt model is being run must be edited in the scripts.
                -Change the MODEL in the codeml control file.
                -Change the outfile name to the null file. 
		
		
		
## getlongesttranscript.py

Gotten from online (link at the top of the script). Stores all the transcripts in the dictionary associated with each genes. Stores the longest transcript.
run with command: cat filename.gff | python3 /home/leann/lib/ortho_finder_butterflies/scripts/getlongesttranscript.py | cut -f2

        ***NOTE: "cut -f2" is optional. Without that option, all four columns of information about the transcript will print. f2 specifically sprints out the longest transcript ids.
                f1, f3, and f4 will print out the other information individually. The list printed to the screen can be fed into a file using '>'. 

## gtf_getlongest.py
Edit of getlongestranscript.
Runs the same but takes a gtf file instead of gff3 file.

## make_new_proteome.py

input format: python3 make_new_proteome.py [protein file name] [list of longest transcript file name] [desired outputfile name]
This script cross references the list of the longest transcripts with the record id's in the protein file. It then writes out the
records of the all the proteins that match the longest trancripts.


## longest_pipeline.sh

Format to run: needs a file filled with directories named after the respective species. 
Files should be name: speciesname.faa and speciesname.gff.
This script will run getlongesttranscript.py and make_new_proteomes together in a pipeline. 

Con: Does not work for every proteome annotation format. Most likely better to do this manually. 




	

