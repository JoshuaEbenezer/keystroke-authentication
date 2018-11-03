# Extracts hold times, latencies; stores them in corresponding folders

import os
from datetime import datetime


rolls = os.listdir('output')
for rollnum in rolls:
	os.mkdir(rollnum)
	moods = os.listdir('output/'+rollnum)
	for moodnum in moods:
		os.mkdir(rollnum+'/'+moodnum[:-4])
		os.mkdir(rollnum+'/'+moodnum[:-4]+'/Hold times')
		os.mkdir(rollnum+'/'+moodnum[:-4]+'/Latencies')
		f = open('output/'+rollnum+'/'+moodnum,'r')
		f_list = f.readlines()
		f_list = [x[:-1] for x in f_list]
		if f_list[-1]=='\n':
			f_list.pop()
		KeyUps = [x for x in f_list if 'KeyUp' in x]
		KeyDowns = [x for x in f_list if 'KeyDown' in x]

		# Extracting the timestamp and key (making lists of ups and downs)
		tups =  [item[-23:-2] + '000' for item in KeyUps]
		tdowns =  [item[-23:-2] + '000' for item in KeyDowns]
		try:
			letterup =  [item[-25].upper() for item in KeyUps]
		except: 
			print('Error in '+rollnum+'/'+moodnum+' CHECK LINE ' +str(2*KeyUps.index(item)) )
		try:
			letterdown = [item[-25].upper() for item in KeyDowns]
		except:
			print('Error in '+rollnum+'/'+moodnum+' CHECK LINE ' +str(2*KeyDowns.index(item)) )
		
		# For Python 3 and above use the code below
		# tups =  [item[-22:-1] + '000' for item in KeyUps]
		# tdowns =  [item[-22:-1] + '000' for item in KeyDowns]
		# letterup =  [item[-24] for item in KeyUps]
		# letterdown = [item[-24] for item in KeyDowns]
			
		
		for i in range(0,len(tups)-1):
			t = i
			t1 = datetime.strptime(tdowns[i], "%d:%m:%y:%H:%M:%S:%f")
			# If the bad case occurs where the up order isnt the same as the down order
			if letterup[t] != letterdown[i]:
				j = i
				# Check if keyup is to the right of keydown
				if i == len(tups)-1:
					j = 0
				while j<len(tups)-1 and letterdown[i]!= letterup[j] and i!=len(tups)-1:
					j = j+1
				tj = datetime.strptime(tups[j], "%d:%m:%y:%H:%M:%S:%f")
				k = i
				# Check if keyup is to the left of keydown
				if i == 0:
					k = len(tups)-1
				while k>=1 and letterdown[i]!= letterup[k] and i!=0:
					k = k-1
				tk = datetime.strptime(tups[k], "%d:%m:%y:%H:%M:%S:%f")
				# Take the min of left and right distances if both distances can be valid
				if (tk-t1).total_seconds()>0 and (tj-t1).total_seconds()>0:
					if abs(j-i)<abs(i-k):
						t = j
					else:
						t = k
				elif (tk-t1).total_seconds()<0:
					t = j
				else:
					t = k
			t2 = datetime.strptime(tups[t], "%d:%m:%y:%H:%M:%S:%f")
			# Latency calculation
			if i!=len(tups)-1:
				t3 = datetime.strptime(tdowns[i+1], "%d:%m:%y:%H:%M:%S:%f")
				latency = t3-t1
				latency = latency.total_seconds()
				try:
					f = open(rollnum+'/'+moodnum[:-4]+"/Latencies/"+letterdown[i] + letterdown[i+1] + ".txt", "a+")
				except:
					continue
				f.write(str(latency) + "\n")	
				f.close()
			# Hold time calculation
			hold_time = t2-t1
			hold_time = hold_time.total_seconds()
			try:
				f = open(rollnum+'/'+moodnum[:-4]+"/Hold times/" + letterdown[i] + ".txt", "a+")
			except:
				continue
			f.write(str(hold_time) + "\n")	
			f.close()