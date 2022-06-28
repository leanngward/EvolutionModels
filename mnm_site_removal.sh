#!/bin/bash

#Run HYPHY multi-hit to get sites where MNM models fit better
hyphy FitMultiModel.bf --alignment mlh1.fasta

#Pull sites from resulting JSON file
in2csv -k "Site substitutions" mlh1.fasta.FITTER.json > mlh1_results.csv

#Remove first line from results file
sed 1d mlh1_results.csv > mlh1_sitelist.txt

#Increment each value by 1, because JSON files return the incorrect site number for some reason
awk -F, '{$1=$1+1;print}' OFS=, mlh1_sitelist.txt > mlh1_mnm_sites.txt
