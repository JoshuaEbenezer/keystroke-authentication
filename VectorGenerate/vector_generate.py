# Stores the list of input points with respect to the features mentioned in a file
# The remaining files in the folder are for running a toy example.
# common_feat.txt contains the list of common features
# Hold times and Latencies folders contain the respective times for a user

import itertools
import os
import pickle
import numpy
import random
import numpy as np


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
      if random.randrange(num): continue
      line = aline
    return line
f = open('common_feat.txt','r')
f_list = f.readlines()
f_list = [x[:-1] for x in f_list]
if f_list[-1]=='\n':
    f_list.pop()
# f_list contains common features
rolls = os.listdir('output')

random_flist = []

random_indice = random.sample(range(0, 24), 24)

for ind in range(len(random_indice)):
    random_flist.append(f_list[random_indice[ind]])

print(random_flist)


for rollnum in rolls:
    # Extracting the hold times and latencies from the files
    hold_list = os.listdir('output'+'/'+rollnum+'/'+'Hold times')
    lat_list = os.listdir('output'+'/'+rollnum+'/'+'Latencies')
    total_list = hold_list + lat_list
    # Common feature
    total_list = [x for x in random_flist if x in total_list]
    # print(total_list)
    # List of lists of latencies and hold times
    l = []
    feat_vec = np.zeros((256,24))
    # Parsing the files to generate l
    for i in range(256):
        file_no=0
        for x in total_list:            
            inner_list = []
            try:
                with open('output'+'/'+rollnum+'/'+'Hold times/'+x) as f:
                    line = random_line(f)
                    # try:
                    #     inner_list.append([float(elt.strip()) for elt in line.split(' ')])                      
                    # except:
                    #     continue
                feat_vec[i,file_no] = line
            except:
                with open('output'+'/'+rollnum+'/'+'Latencies/'+x) as f:
                    line=random_line(f)
                    # try:
	                   #  inner_list.append([float(elt.strip()) for elt in line.split(' ')])
                    # except:
                    #     continue
                    feat_vec[i,file_no] = line
            file_no+=1



    # print('Row1:',feat_vec[1,:],'Row2:',feat_vec[2,:])    
    with open('./pickled_vectors/'+rollnum+'.pickle', 'wb') as f:
        pickle.dump(feat_vec, f)
