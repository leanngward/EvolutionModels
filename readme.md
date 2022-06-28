# dN-dS-pipeline
As part of my master's thesis at Mississippi State University, I am exploring patterns of molecular evolution in the long-lived Heliconius butterfly. This pipeline will take a set of protein genes files of interest and prepare them to run with the codeml package from PAML.

### 1. For my research, I used the Orthofinder package to create files for each of my single copy genes. From there, copy results file filled with single copy orthogroups into a directory.
        ***Note: If you are not starting from these point, you will need a nucleotide fasta files for each of your genes of interest that containing orthologs
        from your species of interest (not all species have to be present in every gene group.) Each DNA sequence in your files must be named with the following 
        convention: > speciesname_genegroupname
        
        If they are not named as such (results from orthofinder will not be), use step #2. rename_orthogroup_genes.py

### 2. rename_orthogroup_genes.py
        Need: Directory filled with single copy orthogroup fasta files, directory filled with genome files used to run Orthofinder
        Run Command: python3 rename_orthogroup_genes.py [genomes dir] [orthogroup fasta file dir] [output dir name of choice]
                **reminder: make sure to include the last path slash for your directories!
        How it Works: For every file in the single copy orthogroups directory, it searches the record ID's within the file against a dictionary
        created with the genomes. Within the output directory, a new dir for every orthogroup (named with the orthogroup name) is created and
        an edited sequence file is written there. The edited sequence file has the renamed record.id's for each sequence in the format:
        >speciesname_orthogroup.
                **Note: If the original files are not named as [ORTHOGROUP.fa], like 0G0001832.fa, the new directories, files, and record id edits
                        will instead by named with what your file names are. However, the last three characters will be cut off (with the orthogroups,
                        ".fa" is cut off).

### 3. translate_sequences.py
        Need: Directory filled with your gene group (or orthogroups) directories. There must be one nucleotide fasta  sequence file in each directory.
        Run Command: python3 translate_sequences.py [outer directory]
        How it Works: Removes stop codons and translates the nucleotide sequence files within each subdirectory. Creates new files named:
        "protein_[filename]"  

### 4. curate_pipeline.sh
        Need: Directory filled with subdirectories, each subdirectory should be named as the ORTHOGROUP/genegroup (the result directory from rename_orthogroup_genes.py).
              Each subdirectory should only contain the nucleotide fasta file and the protein fasta file. Named like they from rename_orthogroup_genes.py and
              translate_sequences.py (for example, OG0001832.fa and protein_OG0001832.fa)
        NOTES: Remember to make the following edits per run: change the out directory location for tree files to be copied to and create that directory
               before before you run it.
               
        Run Command: ./curatepipeline.sh
                ***Note: Must be run in the Directory (still outside the subdirectories)
        How It works: Within each subdirectory it run the following commands:

                        Will only start running on files with "protein_". Be careful not to create duplicates.
                        Runs mafft on the protein files to align them  and output is named as "aligned_protein_[filename]" 
                        Calls Pal2Nal to back-translate the aligned protein files. Output is named "nuc_[filename]_aligned.fasta"
                        Calls iqtree to create trees for "nuc_[filename]_aligned.fasta" and creates "nuc_[filename]_aligned.fasta.nwk"
                        Calls Fasta2Phy to convert the "nuc_[filename]_aligned.fasta" from a fasta to a phylip of the same name.
                        Copies the "nuc_[filename]_aligned.fasta.nwk" to a new subdir (this should be edited by user) with files called "[filename]_tree.nwk"
### 5. check_trees1.py
        Need: You will need a nwk file with a master tree of all the species in your experiment.
                ***Note: Master tree will need to have specific edites. Species in the file must be writen with an underscore following the name. [speciesname]_
                        The species of interest must have a ":2" the species name. All other branch lengths (:###) must be removed.
              You will need ete3 installed. (As of 1/27/2022 for LeAnn: source ~/.bashrc and conda activate ete3 will allow you to run it.)
        Run Command: python3 check_trees1.py [master tree] [tree directory]
        How it Works: Code double checks for spelling errors, etc., by seeing if all the species in the treefiles
        exist in the mastertree by making use of ete3. Helps make sure that both are correct.

### 6. prune_trees2.py
        Need: The directory filled with tree files from the curate_pipeline.sh that has been checked.
              The same master tree file used with check_trees1.py
        Run Command: python3 prune_tree2.py [tree file directory] [desired output directory name] [mastertree]
                ***Notes: Do not create your output directory before running. It does this for you, and will fail if you have already made one.
                          Make sure to include a slash at the end of your paths
        How it Works: Loops through the tree files in the input directory. Creates a pruned tree file with the topology of the given supertree.
                      For use with codeml!
### 7. parse_trees3.py
        Need: The directory filled with pruned tree from prune_trees2.py
        Run Command: python3 parse_trees3.py [pruned tree directory name] [output directory name]
                        ***Note: This creates the directory for you, so if it is already created then delete it or pick new output name.
        How it Works: Final curation step for codeml trees. Adds back the group/gene names to each node in the tree. Changes
                      The 2 to a $1 on the species of interest for the codeml run.

### 8. create_codeml_files.py
        Need: You will need a directory full of gene group subdirectories and a directory of you final tree files. These should be created by the previous scripts.
        Run Command: python3 create_codeml_files.py [directory of group directories] [tree file directory]
        How it Works: This file uses the subdirectory groupname to create codeml control files for both an alternative and null branch model. It also creates
                        .sh files to submit all the control files to the job queue using the "qsub" command. All the files it creates will be in the main 
                        directory, outside the group directories. If all the files don't completely run, the created job files can still be run individually.
                        ***Note: Do not re-run this script unless it fails to run or you will create duplicate files.


### 9. read_codeml_output.py
        Need: Directory of gene group subdirectories and the NAME of the output file you want. It is tab delimited
              so a .tsv file is recommended but not required.
        Run Command: python3 read_codeml_output.py [runfile directory] [results output file name]
        How it Works: This code systematically checks in the subdirectories for the codeml outputs. If it finds one, it stores the appropraite lnl and omega
                        values depending on if it is a null or alternative output file. If it does not find one, it raises a flag to the output screen.
                        It also creates a list called "undonelist.txt" (it is the same everytime and will replace itself when you run it again). The list consists
                        of the appropriate run statement for the file you want, along with the qsub, so that you can directory copy it and run it again (once errors are solved).
                       You can continue running this output until you have your complete results.
                        ***Note: This is designed for how mine are named by the previous scripts: ending in _null.out or _alt.out
                        for the null and alternative models)
