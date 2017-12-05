#Roy David
#Bascriptie
#Geographical Home Location Prediction of a Dutch Twitter user

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

start_time = time.time()
	
print("Descr:	collects and creates datafile used for bathesis")
print("Usage:	python get_data.py")

cred = json.load(open("credentials-roy.json"))
my_authentication = OAuth(cred["ACCESS_TOKEN"], cred["ACCESS_TOKEN_SECRET"], \
			  cred["CONSUMER_KEY"], cred["CONSUMER_SECRET"])

ts = TwitterSearch(access_token=cred["ACCESS_TOKEN"],access_token_secret=cred["ACCESS_TOKEN_SECRET"],
			   consumer_key=cred["CONSUMER_KEY"], consumer_secret=cred["CONSUMER_SECRET"])

regions = ["south","west","east","north"]
news_list = []
random100_list = []
translator = str.maketrans('', '', string.punctuation)
punct = ["…","“","”","‘","’","€"]
provinces = ["groningen","friesland","drenthe","overijssel","gelderland","flevoland","utrecht","noordholland","zuidholland","zeeland","noordbrabant","limburg"]
cities = ["delfzijl","veendam",
"leeuwarden","drachten","sneek","heerenveen",
"assen","emmen","hoogeveen","meppel",
"kampen","zwolle","almelo","hengelo","enschede","deventer",
"zutphen","doetinchem","arnhem","nijmegen","wageningen","apeldoorn",
"emmeloord","lelystad","almere",
"amersfoort",
"hilversum","amstelveen","amsterdam","zaandam","purmerend","haarlem","amstelveen","alkmaar","enkhuizen",
"leiden","alphenaandenrijn","zoetermeer","gouda","zoetermeer","delft","denhaag","rotterdam","dordrecht",
"middelburg","vlissingen","terneuzen",
"bergenopzoom","roosendaal","breda","tilburg","shertogenbosch","denbosch","oss","eindhoven","helmond",
"venlo","roermond","heerlen","maastricht"]

for region in regions:

	print("\n\t",region)
	print("collecting data might take a while...")

	infile = "data-master/uniq_users_{}.txt".format(region)

	uniq_users_region = open(infile).readlines()
	print("len unique users",region,": ",len(uniq_users_region))
	users_region = []
	for line in uniq_users_region:
		line = line.split("\t")
		users_region.append(line[0])

	np.random.seed(1234)
	np.random.shuffle(users_region)

	region_list = []
	
	for user in users_region:
		if len(region_list) != 250:
			### filter retweets, the tweets from emoticons \n, @'s, punctuation and urls and lowercase text ###

			
			try:
				twitter_user_order = TwitterUserOrder(user)

				all_tweets = []

				for tweet in ts.search_tweets_iterable(twitter_user_order):
					if len(all_tweets) != 100:
						if "belgië" not in tweet['user']['location'].lower() and "belgium" not in tweet['user']['location'].lower() and "belgie" not in tweet['user']['location'].lower():
							if "RT" != tweet['text'].split()[0]: # filter retweets by skipping them
								lang = langid.classify(tweet['text'])

								if lang[0] == "nl": # check wether language is Dutch
								
									tweet['text'] = tweet['text'].lower()
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
												
									tweet['text'] = tweet['text'].translate(translator) #rm punctuation
									for p in punct:
										if p in tweet['text']:
											tweet['text'] = tweet['text'].replace(p," ")
									
									txt = []
									for word in tweet['text'].split(): #remove 1 letter "words"
										if len(word) == 1:
											pass
										else:
											txt.append(word)
									tweet['text'] = " ".join(txt)

									# uncomment to only remove provincenames
									#for word in tweet['text'].split():
									#	if word in provinces: #remove provincenames (some overlap with city names)
									#		tweet['text'] = tweet['text'].replace(word,"")
									# comment to only remove provincenames
									for word in tweet['text'].split():
										for prov in provinces: #remove all words with provincenames in them
											for c in cities: #remove all words with citynames in them
												if prov in word or c in word:
													tweet['text'] = tweet['text'].replace(word,"")

									if tweet['text'] != "" and tweet['text'].split() != []:
										dup = False
										for twt in all_tweets: #skip duplicate tweets
											if tweet['text'] == twt['text']:
												dup = True
										if dup == False:
											all_tweets.append(tweet)

					elif len(all_tweets) == 100:
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
						break


			except TwitterSearchException as e: # catch errors
				# uncomment to see error
				#print(e)
				pass
	
		elif len(region_list) == 250:
			print("len region_list: ",len(region_list))
			# uncomment to create file for each region
			#with open(region,"w") as regionfile:
			#	for line in region_list:
			#		regionfile.write(str(line))
			#		regionfile.write("\n")
			for line in region_list:
				news_list.append(line)
			#print("len news: ",len(news_list))
			np.random.seed(1234)
			random25nrs = []
			while len(random25nrs) != 25:
				randomint = np.random.randint(0, 250)
				if randomint not in random25nrs:
					random25nrs.append(randomint)
			#print("len random25nrs: ",len(random25nrs))
			for nr in random25nrs:
				random100_list.append(region_list[nr])
			#print("len random100: ",len(random100_list))
			break
	if len(random100_list) == 100:
		with open("random100","w") as random100file:
			for line in random100_list:
				random100file.write(str(line))
				random100file.write("\n")
	if len(news_list) == 1000:
		np.random.seed(1234)
		np.random.shuffle(news_list)
		with open("news","w") as newsfile:
			for line in news_list:
				newsfile.write(str(line))
				newsfile.write("\n")

print("collecting data done...")

print("\n--- %s seconds ---" % (time.time() - start_time))
