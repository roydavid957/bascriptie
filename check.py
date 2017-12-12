#Roy David
#bascriptie
#word check

import ast
import sys

#Descr:	used for analysis of the most informative features
#	shows tweets with the specific word and label
#	shows frequency of the word in the data
#Usage:	within the code specify which label to look for

if len(sys.argv) == 3:

	f = open(sys.argv[-2],"r").readlines()
	amount = []
	region = []

	# comment/uncomment one of the two to see the amount and all
	# the tweets from that label with a certain word in it
	lbl = ["N","E","S","W"]
	#lbl = ["W"] # specifiy specific label(s)

	w = str(sys.argv[-1]) # specify which word to look for
	for line in f:
		line = line.strip("\n")
		line = ast.literal_eval(line)
		line = [line]
		for l in line:
			for k,v in l.items():
				if l[k]["location"] in lbl:
					region.append(l[k]["location"])
					for tweet in l[k]["text"]:
						for word in tweet.split():
							if word == w:
								print(l[k]["location"],tweet)
								amount.append(tweet)
	print("")
	print("tweets with",w,":",len(amount))

else:
	print("Something went wrong, see usage...")
	print("Usage:\tcheck.py file word")