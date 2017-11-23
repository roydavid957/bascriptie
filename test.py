import numpy as np
import ast
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from nltk import ngrams
from nltk.corpus import stopwords

f = open("news.filtered","r").readlines()

x_train = []
x2_train = []
x3_train = []
y_train = []
n = 2
c = 3
for line in f:
	line = line.strip("\n")
	line = ast.literal_eval(line)
	line = [line]
	for l in line:
		d = {}
		twograms = []
		two_grams = []
		d2 = {}
		trigrams = []
		tri_grams = []
		d3 = {}
		for k,v in l.items():
			y_train.append(l[k]["location"])
			for tweet in l[k]["text"]:
				tweet = [word for word in tweet.split() if word not in stopwords.words('dutch')]
				for word in tweet:
					d[word] = 1
				twograms.append(ngrams(tweet, n))
				for char in twograms:
					for grams in char:
						two_grams.append(grams[0]+"_"+grams[1])
				for grams in two_grams:
					d2[grams] = 1
				trigrams.append(ngrams(tweet, c))
				for char in trigrams:
					for grams in char:
						tri_grams.append(grams[0]+"_"+grams[1]+"_"+grams[2])
				for grams in tri_grams:
					d3[grams] = 1
		x_train.append(d)
		x2_train.append(d2)
		x3_train.append(d3)

y_train_np = np.array(y_train)

#data = x_train
#print("len data: ",len(data))
label_train = y_train_np
#print("len label_train: ",len(label_train))
#data_dev = x_train[500:800]
#print("len data_dev: ",len(data_dev))
#label_dev = y_train_np[500:800]
#print("len label_dev: ",len(label_dev))
#print("")

vectorizer = DictVectorizer()

classifiers = [LogisticRegression(),SVC(),GaussianNB]
x_list = [x_train,x2_train,x3_train]
all_avg_acc_score = []
feat = False
for classifier in classifiers:
	if classifier == classifiers[0]:
		print("\t#####\tLogisticRegression\t#####\n")
	if classifier == classifiers[1]:
		print("\t#####\tSVC\t#####\n")
	if classifier == classifiers[2]:
		print("\t#####\tGaussianNB\t#####\n")
	for x in x_list:
		if x == x_train:
			print("\t#####\tUNIGRAMS\t#####\n")
		if x == x2_train:
			print("\t#####\tBIGRAMS\t#####\n")
		if x == x3_train:
			print("\t#####\tTRIGRAMS\t#####\n")
		X_train = vectorizer.fit_transform(x, label_train)
		#X_dev = vectorizer.transform(data_dev)

		"""KFOLD"""
		print("KFold, n=10:")
		kfold = StratifiedKFold(n_splits=10, shuffle=True)
		acc_score = 0
		acc_list = []
		for train_index, test_index in kfold.split(X_train, label_train):
			#print("TRAIN:", train_index, "TEST:", test_index)
			X_trn, X_tst = X_train[train_index], X_train[test_index]
			y_trn, y_tst = label_train[train_index], label_train[test_index]
			classifier.fit(X_trn, y_trn)
			predicted_y = classifier.predict(X_tst)
			#print("predicted_y: ",len(predicted_y),"\n",predicted_y)
			#print("")
			acc = accuracy_score(y_tst, predicted_y)
			#print("accuracy_score:\n",acc)
			acc_score += float(acc)
			acc_list.append(float(acc))
			if feat == True:
				print("classification_report:\n",classification_report(y_tst, predicted_y))
				print("")
				print(classifier.classes_)
				print(confusion_matrix(y_tst, predicted_y, labels=["E", "N", "S", "W"]))
				print("")
		all_avg_acc_score.append((acc_score / (len(acc_list))))
		print("\tRESULTS:")
		print("avg accuracy_score: ",(acc_score / (len(acc_list))))
		print("acc_list: ",len(acc_list),"\n\t",acc_list)
		print("")
		"""KFOLD"""

		"""MOST INF FEAT"""
		if feat == True:
			#def show_most_informative_features(vectorizer, classifier, n=20):
			print("Most informative features:")
			n=20
			feature_names = vectorizer.get_feature_names()
			coefs_with_fns = sorted(zip(classifier.coef_[0], feature_names))
			top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
			for (coef_1, fn_1), (coef_2, fn_2) in top:
				print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))
			print("")
		"""MOST INF FEAT"""
	
		#classifier.fit(X_train, label_train)
		#print("classifier:\n",classifier)
		#print("")
		#predicted_y = classifier.predict(X_dev)
		#print("predicted_y: ",len(predicted_y),"\n",predicted_y)
		#print("")
		#print("accuracy_score:\n",accuracy_score(label_dev, predicted_y))
		#print("classification_report:\n",classification_report(label_dev, predicted_y))
print("\tAVERAGE ACC:")
for score in all_avg_acc_score:
	if score == all_avg_acc_score[0]:
		print("LogiscticRegression: ", score)
	if score == all_avg_acc_score[1]:
		print("SVC: ",score)
	if score == all_avg_acc_score[2]:
		print("GuassianNB: ",score)
print("done...")
