#Roy David
#Bascriptie
#Geographical Home Location Prediction of a Dutch Twitter user

#Descr:	code for the experiments for the bathesis
#	using StratifiedKFold
#	using the classifiers: LogisticRegression and LinearSVC
#	outputs f1_score, classification_report, confusion_matrix
#Usage:	python test.py

import numpy as np
import ast
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from nltk import ngrams
from nltk.corpus import stopwords
import time

start_time = time.time()

print("Descr:\tdoes the experiments for the bathesis")
print("\tusing StratifiedKFold")
print("\tusing the classifiers: LogisticRegression and LinearSVC")
print("\tusing uni-, bi-, trigrams as features")
print("\toutputs f1_score, classification_report, confusion_matrix")
print("Usage:\tpython test.py")
print("")

f = open("news.uniq","r").readlines()

print("creating X's and Y's, might take some time...")
print("")

x_train = []
x2_train = []
x3_train = []
x12_train = []
y_train = []
n = 2
c = 3
for line in f:
	line = line.strip("\n")
	line = ast.literal_eval(line)
	line = [line]
	for l in line:
		d1 = {}
		twograms = []
		two_grams = []
		d2 = {}
		trigrams = []
		tri_grams = []
		d3 = {}
		d12 = {}
		for k,v in l.items():
			y_train.append(l[k]["location"])
			for tweet in l[k]["text"]:
				tweet = [word for word in tweet.split() if word not in stopwords.words('dutch')]
				for word in tweet: #create unigrams
					d1[word] = 1 
					d12[word] = 1
				twograms.append(ngrams(tweet, n))
				for char in twograms: #create bigrams
					for grams in char:
						two_grams.append(grams[0]+"_"+grams[1])
				for grams in two_grams:
					d2[grams] = 1
					d12[grams] = 1
				trigrams.append(ngrams(tweet, c))
				for char in trigrams: #create trigrams
					for grams in char:
						tri_grams.append(grams[0]+"_"+grams[1]+"_"+grams[2])
				for grams in tri_grams:
					d3[grams] = 1
		x_train.append(d1)
		x2_train.append(d2)
		x3_train.append(d3)
		x12_train.append(d12)

y_train_np = np.array(y_train)

label_train = y_train_np

vectorizer = DictVectorizer()

classifiers = [LogisticRegression(),LinearSVC()]
x_list = [x_train,x2_train,x3_train,x12_train]
top_f1_score = 0
for classifier in classifiers:
	if classifier == classifiers[0]:
		print("\t#####\tLogisticRegression\t#####\n")
	if classifier == classifiers[1]:
		print("\t#####\tLinearSVC\t#####\n")
	for x in x_list:
		if x == x_train:
			print("\t#####\tUNIGRAMS\t#####\n")
		if x == x2_train:
			print("\t#####\tBIGRAMS\t#####\n")
		if x == x3_train:
			print("\t#####\tTRIGRAMS\t#####\n")
		if x == x12_train:
			print("\t#####\tUNI+BIGRAMS\t#####\n")
		X_train = vectorizer.fit_transform(x, label_train)

		"""KFOLD"""
		print("KFold, n=10:")
		kfold = StratifiedKFold(n_splits=10, shuffle=True)
		f1score = 0
		f1_list = []
		for train_index, test_index in kfold.split(X_train, label_train):
			X_trn, X_tst = X_train[train_index], X_train[test_index]
			y_trn, y_tst = label_train[train_index], label_train[test_index]
			classifier.fit(X_trn, y_trn)
			predicted_y = classifier.predict(X_tst)
			#print("predicted_y: ",len(predicted_y),"\n",predicted_y)
			#print("")
			f1 = f1_score(y_tst, predicted_y, average='micro')
			f1score += f1
			f1_list.append(f1)
			#print("classification_report:\n",classification_report(y_tst, predicted_y))
			#print("")
			#print(classifier.classes_)
			#print(confusion_matrix(y_tst, predicted_y, labels=["E", "N", "S", "W"]))
			#print("")
		print("\tRESULTS:")
		avg_f1_score = f1score / len(f1_list)
		print("avg f1_score: ",avg_f1_score)
		print("f1_list: ",len(f1_list),"\n\t",f1_list)
		print("")
		"""KFOLD"""

		"""MOST INF FEAT"""
		#n=10
		#feature_names = vectorizer.get_feature_names()
		#print("feature_names")
		#coefs_with_fns = sorted(zip(classifier.coef_[0], feature_names))
		#top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
		#for (coef_1, fn_1), (coef_2, fn_2) in top:
		#	print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))
		#print("")
		#if avg_f1_score > top_f1_score:
		#	top_f1_score = avg_f1_score
		print("Most informative features:")
		n=10
		feature_names = vectorizer.get_feature_names()
		for i in range(0,len(classifier.coef_)):
			coefs_with_fns = sorted(zip(classifier.coef_[i], feature_names))
			top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
			print("i",i,classifier.classes_[i])
			for (coef_1, fn_1), (coef_2, fn_2) in top:
				print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))
		print("")
		"""MOST INF FEAT"""

print("done...")

print("\n--- %s seconds ---" % (time.time() - start_time))
