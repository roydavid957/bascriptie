# bascriptie
Roy David
s2764989

This repository contains the code used for the Bachelor thesis course for Information Science at the University of Groningen (RUG).

It contains the following files:
get_uniq_users: contains the Linux commands in order to get the users used to collect the data with. 
After running the Linux commands make sure to put the files gotton from the commands into a directory called:
data-master
data-master: should at least include: uniq_users_north.txt, uniq_users_east.txt, uniq_users_west.txt, uniq_users_south.txt
This is needed because get_data_prov.py and get_data_city.py both call "data-master/uniq_users_(region).txt" (region: either: north, south, east, west).

For the following two python programs you need to have your own Twitter credentials file:

get_data_prov.py: uses the files in the directory data-master created by the Linux commands in get_uniq_users, to get the dataset without provinces in the tweets. Creates files: news.prov and random100.prov, news.prov can be used by test.py to get the results, random100.prov for the manual distant supervision check. Usage: python get_data_prov.py

get_data_city.py: uses the files in the directory data-master created by the Linux commands in get_uniq_users, to get the dataset without provinces and cities in the tweets. Creates files: news.city and random100.city, news.city can be used by test.py to get the results, random100.city for the manual distant supervision check. Usage: python get_data_city.py

test.py: does the experiments on either the news.prov file from get_data_prov.py, or the news.city file from get_data_city.py. Does the experiments using the Logistic Regression classfier and the Linear SVC classifier using uni-grams, bi-grams, tri-grams and uni-+bi-grams as features. Usage: python test.py file (file = news.city or news.prov, from get_data_city.py or get_data_prov.py)

check.py: used for analysis of the most informative features from test.py. Shows the tweet with the word in it and the frequency. Usage: python check.py word
