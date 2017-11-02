import json
from TwitterSearch import TwitterUserOrder, TwitterSearch, TwitterSearchException
from twitter import OAuth
import langid
import string
import time
import numpy as np
import random
import time

start_time = time.time()
cred = json.load(open("credentials-roy.json"))
my_authentication = OAuth(cred["ACCESS_TOKEN"], cred["ACCESS_TOKEN_SECRET"], \
			  cred["CONSUMER_KEY"], cred["CONSUMER_SECRET"])

ts = TwitterSearch(access_token=cred["ACCESS_TOKEN"],access_token_secret=cred["ACCESS_TOKEN_SECRET"],
		       consumer_key=cred["CONSUMER_KEY"], consumer_secret=cred["CONSUMER_SECRET"])

# set to True to enable datacollection, False to skip for that region
E = True # East
W = True # West
N = True # North
S = True # South
A = True # All data (set all to True to enable file w/ all data)

if E == True:
	#########################################################################################################EAST
	# uncomment to enable creating an extra file containing only data for this region
	east = open('east.txt', 'w')
	print("\n\tEAST")
	print("collecting data might take a while...")
	uniq_users_east = open("data-master/uniq_users_east.txt").readlines()
	users_east = []
	for line in uniq_users_east:
		line = line.split("\t")
		users_east.append(line[0])

	np.random.seed(1234)
	np.random.shuffle(users_east)


	east_list = []

	for user in users_east:
		if len(east_list) != 25000:
			### filter retweets, the tweets from emoticons \n, @'s, punctuation and urls and lowercase text ###

			punctuation_list = ["!","@","$","%","^","&","*","(",")","-","_","=","+","`","~","[","{","]","}","\\","|",";",":","'",'"',",","<",".",">","/","?"] # all punctuation except "#"
			try:
				twitter_user_order = TwitterUserOrder(user)

				all_tweets = []
			
				for tweet in ts.search_tweets_iterable(twitter_user_order):
					if len(all_tweets) != 100:
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

								if "\n" in tweet['text']:
									tweet['text'] = tweet['text'].replace("\n"," ") # replace every \n in tweet with space

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
						for tweet in all_tweets:
							east_list.append(tweet['user']['screen_name']+"\t"+tweet['text']+"\t"+tweet['user']['location']+"\n")
						break


			except TwitterSearchException as e: # catch errors
				print(e)
				#pass
				
		elif len(east_list) == 25000:
			np.random.seed(1234)
			np.random.shuffle(east_list)
			print("len east_list: ",len(east_list))
			for line in east_list:
				east.write(line)
			break

	print("collecting data done...")

if W == True:
	#########################################################################################################WEST
	# uncomment to enable creating an extra file containing only data for this region
	west = open('west.txt', 'w')
	print("\n\tWEST")

	uniq_users_west = open("data-master/uniq_users_west.txt").readlines()
	users_west = []
	for line in uniq_users_west:
		line = line.split("\t")
		users_west.append(line[0])

	np.random.seed(1234)
	np.random.shuffle(users_west)


	west_list = []

	for user in users_west:
		if len(west_list) != 25000:
			### filter retweets, the tweets from emoticons \n, @'s, punctuation and urls and lowercase text ###

			punctuation_list = ["!","@","$","%","^","&","*","(",")","-","_","=","+","`","~","[","{","]","}","\\","|",";",":","'",'"',",","<",".",">","/","?"] # all punctuation except "#"
			try:
				twitter_user_order = TwitterUserOrder(user)

				all_tweets = []
			
				for tweet in ts.search_tweets_iterable(twitter_user_order):
					if len(all_tweets) != 100:
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

								if "\n" in tweet['text']:
									tweet['text'] = tweet['text'].replace("\n"," ") # replace every \n in tweet with space

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
						for tweet in all_tweets:
							west_list.append(tweet['user']['screen_name']+"\t"+tweet['text']+"\t"+tweet['user']['location']+"\n")
						break


			except TwitterSearchException as e: # catch errors
				print(e)
				#pass
				
		elif len(west_list) == 25000:
			np.random.seed(1234)
			np.random.shuffle(west_list)
			print("len west_list: ",len(west_list))
			for line in west_list:
				west.write(line)
			break

	print("collecting data done...")

if N == True:
	#########################################################################################################NORTH
	# uncomment to enable creating an extra file containing only data for this region
	north = open('north.txt', 'w')
	print("\n\tNORTH")

	uniq_users_north = open("data-master/uniq_users_north.txt").readlines()
	users_north = []
	for line in uniq_users_north:
		line = line.split("\t")
		users_north.append(line[0])

	np.random.seed(1234)
	np.random.shuffle(users_north)


	north_list = []

	for user in users_north:
		if len(north_list) != 25000:
			### filter retweets, the tweets from emoticons \n, @'s, punctuation and urls and lowercase text ###

			punctuation_list = ["!","@","$","%","^","&","*","(",")","-","_","=","+","`","~","[","{","]","}","\\","|",";",":","'",'"',",","<",".",">","/","?"] # all punctuation except "#"
			try:
				twitter_user_order = TwitterUserOrder(user)

				all_tweets = []
			
				for tweet in ts.search_tweets_iterable(twitter_user_order):
					if len(all_tweets) != 100:
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

								if "\n" in tweet['text']:
									tweet['text'] = tweet['text'].replace("\n"," ") # replace every \n in tweet with space

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
						for tweet in all_tweets:
							north_list.append(tweet['user']['screen_name']+"\t"+tweet['text']+"\t"+tweet['user']['location']+"\n")
						break


			except TwitterSearchException as e: # catch errors
				print(e)
				#pass
				
		elif len(north_list) == 25000:
			np.random.seed(1234)
			np.random.shuffle(north_list)
			print("len north_list: ",len(north_list))
			for line in north_list:
				north.write(line)
			break

	print("collecting data done...")

if S == True:
	#########################################################################################################SOUTH
	# uncomment to enable creating an extra file containing only data for this region
	south = open('south.txt', 'w')
	print("\n\tSOUTH")

	uniq_users_south = open("data-master/uniq_users_south.txt").readlines()
	users_south = []
	for line in uniq_users_south:
		line = line.split("\t")
		users_south.append(line[0])

	np.random.seed(1234)
	np.random.shuffle(users_south)


	south_list = []

	for user in users_south:
		if len(south_list) != 25000:
			### filter retweets, the tweets from emoticons \n, @'s, punctuation and urls and lowercase text ###

			punctuation_list = ["!","@","$","%","^","&","*","(",")","-","_","=","+","`","~","[","{","]","}","\\","|",";",":","'",'"',",","<",".",">","/","?"] # all punctuation except "#"
			try:
				twitter_user_order = TwitterUserOrder(user)

				all_tweets = []
			
				for tweet in ts.search_tweets_iterable(twitter_user_order):
					if len(all_tweets) != 100:
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

								if "\n" in tweet['text']:
									tweet['text'] = tweet['text'].replace("\n"," ") # replace every \n in tweet with space

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
						for tweet in all_tweets:
							south_list.append(tweet['user']['screen_name']+"\t"+tweet['text']+"\t"+tweet['user']['location']+"\n")
						break


			except TwitterSearchException as e: # catch errors
				print(e)
				#pass
				
		elif len(south_list) == 25000:
			np.random.seed(1234)
			np.random.shuffle(south_list)
			print("len south_list: ",len(south_list))
			for line in south_list:
				south.write(line)
			break

	print("collecting data done...")

if A == True:
	print("\n\tALL DATA")
	print("putting east-, west-, north-, southlist into one...")
	all_data = open('all_data.txt', 'w')
	all_data_list = []
	for line in east_list:
		all_data_list.append(line)
	for line in west_list:
		all_data_list.append(line)
	for line in north_list:
		all_data_list.append(line)
	for line in south_list:
		all_data_list.append(line)
	print("done...")
	print("len all_data_list: ",len(all_data_list))
	print("shuffling data...")
	np.random.seed(1234)
	np.random.shuffle(all_data_list)
	print("writing data to file...")
	for line in all_data_list:
		all_data.write(line)
	print("done...")
	print("collecting data done...")

print("\n--- %s seconds ---" % (time.time() - start_time))


