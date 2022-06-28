import sys

seq_dict = {}
with open(sys.argv[1]) as f:
	for line in f:
		line = line.strip()
		if line.startswith('>'):
			header = line.replace('>', '')
			seq_dict[header] =''
		else:
			seq_dict[header] += line

length = 0
count = 0

while count <= 1:
	for seq in seq_dict:
		length = len(seq_dict[seq])
		count += 1

print('{}{} {}'.format(' ', len(seq_dict), length))

for seq in seq_dict:
	print("{}  {}".format(seq, seq_dict[seq]))

