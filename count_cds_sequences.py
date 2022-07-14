#Writing this quick script to determine how many CDS sequences are in my CDS files

import sys
from Bio import SeqIO

infile = sys.argv[1]

count = 0
for record in SeqIO.parse(infile, "fasta"):
	count += 1


print(count)
