#Roy David
#Bascriptie

#Descr:	collects and creates datafile used for bathesis
#Usage:	python get_data.py

import json
from TwitterSearch import TwitterUserOrder, TwitterSearch, TwitterSearchException
from twitter import OAuth
import langid
import string
import time
import numpy as np
import random
import time
import sys

start_time = time.time()

#if len(sys.argv) == 2:
	
print("Descr:	collects and creates datafile used for bathesis")
print("Usage:	python get_data.py")

cred = json.load(open("credentials-roy.json"))
my_authentication = OAuth(cred["ACCESS_TOKEN"], cred["ACCESS_TOKEN_SECRET"], \
			  cred["CONSUMER_KEY"], cred["CONSUMER_SECRET"])

ts = TwitterSearch(access_token=cred["ACCESS_TOKEN"],access_token_secret=cred["ACCESS_TOKEN_SECRET"],
			   consumer_key=cred["CONSUMER_KEY"], consumer_secret=cred["CONSUMER_SECRET"])

regions = ["north","east","west","south"]
news_list = []
random100_list = []

punctuation_list = ["!","@","$","%","^","&","*","(",")","-","_","=","+","`","~","[","{","]","}","\\","|",";",":","'",'"',",","<",".",">","/","?"] # all punctuation except "#"

for region in regions:

	#print("\n\t",sys.argv[-1])
	print("\n\t",region)
	print("collecting data might take a while...")

	#infile = "data-master/uniq_users_{}.txt".format(sys.argv[-1])
	infile = "data-master/uniq_users_{}.txt".format(region)

	uniq_users_region = open(infile).readlines()
	users_region = []
	for line in uniq_users_region:
		line = line.split("\t")
		users_region.append(line[0])

	np.random.seed(1234)
	np.random.shuffle(users_region)

	region_list = []

	for user in users_region:
		if len(region_list) != 250:
		#if len(region_list) != 25:
			### filter retweets, the tweets from emoticons \n, @'s, punctuation and urls and lowercase text ###

			
			try:
				twitter_user_order = TwitterUserOrder(user)

				all_tweets = []

				for tweet in ts.search_tweets_iterable(twitter_user_order):
					if len(all_tweets) != 100:
					#if len(all_tweets) != 10:
						if "belgië" not in tweet['user']['location'].lower() and "belgium" not in tweet['user']['location'].lower() and "belgie" not in tweet['user']['location'].lower():
							if "RT" != tweet['text'].split()[0]: # filter retweets by skipping them
								lang = langid.classify(tweet['text'])

								if lang[0] == "nl": # check wether language is Dutch

									if "é" in tweet['text'] or "á" in tweet['text'] or "ó" in tweet['text'] or "ú" in tweet['text'] or "í" in tweet['text']: # change é etc to e etc to keep word after encoding
										for word in tweet['text'].split():
											for letter in word:
												if letter == "é":
													tweet['text'] = tweet['text'].replace(letter,"e")
												if letter == "á":
													tweet['text'] = tweet['text'].replace(letter,"a")
												if letter == "ó":
													tweet['text'] = tweet['text'].replace(letter,"o")
												if letter == "ú":
													tweet['text'] = tweet['text'].replace(letter,"u")
												if letter == "í":
													tweet['text'] = tweet['text'].replace(letter,"i")

									tweet['text'] = tweet['text'].encode('ascii','ignore').decode("utf-8").lower() # filter emoticons like "\ud*" etc

									if "\n" in tweet['text']: # replace every \n in tweet with space
										for word in tweet['text'].split():
											tweet['text'] = tweet['text'].replace("\n"," ")
						
									if "\r" in tweet['text']: # replace every \r in tweet with space
										for word in tweet['text'].split():
											tweet['text'] = tweet['text'].replace("\r"," ")

									if "http" in tweet['text']: # remove url from tweet (by replacing with nothing)
										for word in tweet['text'].split():
											if "http" in word:
												tweet['text'] = tweet['text'].replace(word,"")

									if "@" in tweet['text']: # remove "@" from tweet (by replacing with nothing)
										for word in tweet['text'].split():
											if "@" in word:
												tweet['text'] = tweet['text'].replace(word,"")

									for item in punctuation_list: # remove all punctuation except "#"
										if item in tweet['text']:
											tweet['text'] = tweet['text'].replace(item," ")

									if tweet['text'] != "" and tweet['text'].split() != []:
										all_tweets.append(tweet)

					elif len(all_tweets) == 100:
					#elif len(all_tweets) == 10:
						for tweet in all_tweets:
							init = False
							d = {}
							d[tweet['user']['screen_name']] = {'text': [tweet['text']], 'location': region[0].upper()}
							for dic in region_list:
								if tweet['user']['screen_name'] in dic:
									dic[tweet['user']['screen_name']]['text'].append(tweet['text'])
									init = True
							if init == False:
								region_list.append(d)
							#region_list.append(tweet['user']['screen_name']+"\t"+tweet['text']+"\t"+tweet['user']['location'])
						break


			except TwitterSearchException as e: # catch errors
				print(e)
				#pass
	
		elif len(region_list) == 250:
		#elif len(region_list) == 25:
			#np.random.seed(1234)
			#np.random.shuffle(region_list)
			print("len region_list: ",len(region_list))
			with open(region,"w") as outfile:
				for line in region_list:
					outfile.write(str(line))
					outfile.write("\n")
			for line in region_list:
				news_list.append(line)
			print("len news: ",len(news_list))
			np.random.seed(1234)
			random25nrs = []
			while len(random25nrs) != 25:
				randomint = np.random.randint(0, 250)
				#randomint = np.random.randint(0, 25)
				if randomint not in random25nrs:
					random25nrs.append(randomint)
			print("len random25nrs: ",len(random25nrs))
			for nr in random25nrs:
				random100_list.append(region_list[nr])
			print("len random100: ",len(random100_list))
			break
	if len(random100_list) == 100:
	#if len(random100_list) == 8:
		with open("random100","w") as random100file:
			for line in random100_list:
				random100file.write(str(line))
				random100file.write("\n")
	if len(news_list) == 1000:
	#if len(news_list) == 100:
		np.random.seed(1234)
		np.random.shuffle(news_list)
		with open("news","w") as newsfile:
			for line in news_list:
				newsfile.write(str(line))
				newsfile.write("\n")

print("collecting data done...")

#else:
#	print("Something went wrong, please try again...")
#	print("Usage:	python get_user_tweets.py north/east/west/south")

print("\n--- %s seconds ---" % (time.time() - start_time))