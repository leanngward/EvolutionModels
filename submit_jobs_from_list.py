import sys
import subprocess
#Provide the name of list with .sh files
inName = sys.argv[1]

#Provide the file line range that you want to run
#Format as start value, then a space, and then the end value
inStart = sys.argv[2]
inEnd = sys.argv[3]

inFile = open(inName,'r')
count = 0

#make the list of numbers
numList = []
for i in range(int(inStart),int(inEnd)+1):
	numList.append(i)

print(numList)
for line in inFile.readlines():
	count += 1
	line = line.strip()
	if count in numList:
		subprocess.call(["qsub",line])
