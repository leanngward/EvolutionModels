#!/bin/bash

for f in *
do
	GENENAME="$f"
	echo $GENENAME
	if [ -d $f ];then
		cd $f
		for files in *
		do
			if [[ "$files" == *"FITTER.json"* ]];then
				in2csv -k "Site substitutions" "$files" > "${GENENAME}_FITTER.csv"
				sed 1d "${GENENAME}_FITTER.csv" > "${GENENAME}_FITTER_sitelist.txt"
				awk -F, '{$1=$1+1;print}' OFS=, "${GENENAME}_FITTER_sitelist.txt" > "${GENENAME}_FITTER_mnm_sites.txt"
			fi
		done
		cd ..
	fi
done
#Pull sites from resulting JSON file
#in2csv -k "Site substitutions" mlh1.fasta.FITTER.json > mlh1_results.csv

#Remove first line from results file
#sed 1d mlh1_results.csv > mlh1_sitelist.txt

#Increment each value by 1, because JSON files return the incorrect site number for some reason
#awk -F, '{$1=$1+1;print}' OFS=, mlh1_sitelist.txt > mlh1_mnm_sites.txt
