# AUTHOR - Joshua Peter Ebenezer
# DATE OF CREATION - Oct 2nd, 2018

import os
from collections import Counter
import string

# file that contains the list of the common features
f = open("common_feat.txt", "w+")

names = list()

# ./data is expected to contain different folders of the format 
# Roll No
#|--Happy
#	|--Hold times
#   	|--A.txt, B.txt, C.txt.....Z.txt
# 	|--Latencies
#		|--AA.txt, AB.txt.....ZZ.txt
#|--Sad
#	|--Hold times
#   	|--A.txt, B.txt, C.txt.....Z.txt
# 	|--Latencies
#		|--AA.txt, AB.txt.....ZZ.txt
#|--Neutral
#	|--Hold times
#   	|--A.txt, B.txt, C.txt.....Z.txt
# 	|--Latencies
#		|--AA.txt, AB.txt.....ZZ.txt

path = './output'


# find the number of students (users) (by counting the number of folders)
file_count = sum(os.path.isdir(os.path.join(path, i)) for i in os.listdir(path))

# find every single txt file in the hold times and latencies folders for ALL roll nos
for root, subdirs, files in os.walk(path):
	for filename in files:
		names.append(filename)

# count the occurrences of each txt file in the above list
c = Counter(names)

# find all valid filenames
single_textnames = [i + '.txt' for i in (string.ascii_uppercase[:14])]
double_textnames = [i+j+'.txt' for i in (string.ascii_uppercase[:14]) for j in (string.ascii_uppercase[:14])]
textnames = single_textnames+double_textnames

# go through all valid filenames and find out how many of them are in the subdirectories
for name in textnames:
	if (c[name] == file_count):		# if this number is equal to the number of roll numbers, it is present for all users, and belongs to the common subset
		f.write("%s\n" % name)		# hence, write out as part of the common subset
f.close()
