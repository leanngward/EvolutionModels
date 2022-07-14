
#!/bin/bash


for f in *                 #loops through all of the files in the working directory
do
	GENENAME="$f"
	echo $GENENAME
	if [ -d $f ];then                       #check if the files is actually a directory. all the genes should have their own directory. no other directories should be present.
		cd $f 
		for files in *
		do
#			echo "$files"
			if [[ "$files" == *"protein"* ]];then   ###the program will run mafft, pal2nal, and iqtree as long as the appropriate file "protein_*genename*_final.fasta" is in the directory
				module load mafft
				mafft --localpair --maxiterate 1000 --amino "$files" > "aligned_$files"
				perl /scratch/Hoffmann/leann/evomodel_scripts/pal2nal.v14/pal2nal.pl "aligned_$files" "${GENENAME}.fa" -output fasta > "nuc_${GENENAME}_aligned.fasta"
				module load Iq-Tree/2.0
				iqtree -s "nuc_${GENENAME}_aligned.fasta" -nt 3
#				perl /home/leann/lib/Fasta2Phylip.pl "nuc_${GENENAME}_aligned.fasta" "nuc_${GENENAME}_aligned.phy"   #this transform the fasta alignment into a phylip file for codeml
				python /scratch/Hoffmann/leann/evomodel_scripts/fasta2phy.py "nuc_${GENENAME}_aligned.fasta" > "nuc_${GENENAME}_aligned.phy"
				cp "nuc_${GENENAME}_aligned.fasta.treefile" /scratch/Hoffmann/leann/poly_testgroups_run5/original_treefiles/"${GENENAME}_tree.nwk"

			fi
		done
		cd ..
	fi
done
