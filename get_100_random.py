#Roy David
#Bascriptie

import numpy as np
import random

#Descr:	program to select 100 random tweets and 
#	write them to a file (than manually check
#	distant supervision)
#	outputs random numbers used for lines,
#	random 100 data used + file

data = open("all_data.txt").readlines()
np.random.seed(1234)
randlist = []
while len(randlist) != 100:
	randomint = np.random.randint(0, 100000)
	if randomint not in randlist:
		randlist.append(randomint)

print("len randlist: ", len(randlist))
print("randlist: ", randlist)

random100data = []
for nr in randlist:
	random100data.append(data[nr])

print("len random100data: ", len(random100data))
print("random100data: ", random100data)

f = open("random100.txt", "w")

for line in random100data:
	f.write(line)