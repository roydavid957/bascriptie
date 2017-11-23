import numpy as np
import ast
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from nltk import ngrams

f = open("news","r").readlines()

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
				for word in tweet.split():
					d[word] = 1
				twograms.append(ngrams(tweet.split(), n))
				for char in twograms:
					for grams in char:
						two_grams.append(grams[0]+"_"+grams[1])
				for grams in two_grams:
					d2[grams] = 1
				trigrams.append(ngrams(tweet.split(), c))
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

x_list = [x_train,x2_train,x3_train]
for x in x_list:

	X_train = vectorizer.fit_transform(x, label_train)
	#X_dev = vectorizer.transform(data_dev)

	classifier = LogisticRegression()

	"""KFOLD"""
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
		#print("classification_report:\n",classification_report(y_tst, predicted_y))
		#print(confusion_matrix(y_tst, predicted_y))
		#print("")
	print("\tRESULTS:")
	print("avg accuracy_score: ",(acc_score / (len(acc_list))))
	print("acc_list: ",len(acc_list),"\n\t",acc_list)
	print("")
	"""KFOLD"""

	"""MOST INF FEAT"""
	#def show_most_informative_features(vectorizer, classifier, n=20):
	print("Most informative features")
	n=20
	feature_names = vectorizer.get_feature_names()
	coefs_with_fns = sorted(zip(classifier.coef_[0], feature_names))
	top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
	for (coef_1, fn_1), (coef_2, fn_2) in top:
		print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))
	"""MOST INF FEAT"""
	
	#classifier.fit(X_train, label_train)
	#print("classifier:\n",classifier)
	#print("")
	#predicted_y = classifier.predict(X_dev)
	#print("predicted_y: ",len(predicted_y),"\n",predicted_y)
	#print("")
	#print("accuracy_score:\n",accuracy_score(label_dev, predicted_y))
	#print("classification_report:\n",classification_report(label_dev, predicted_y))
print("done...")
