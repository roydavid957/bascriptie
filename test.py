import numpy as np
import ast
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

f = open("news","r").readlines()

x_train = []
y_train = []
for line in f:
	line = line.strip("\n")
	line = ast.literal_eval(line)
	line = [line]
	for l in line:
		d = {}
		for k,v in l.items():
			y_train.append(l[k]["location"])
			for tweet in l[k]["text"]:
				tweet = tweet.split()
				for word in tweet:
					d[word] = 1
		x_train.append(d)

#kfold = KFold(n_splits=10, shuffle=True)
y_train_np = np.array(y_train)

data = x_train[:500]
print("len data: ",len(data))
label_train = y_train_np[:500]
print("len label_train: ",len(label_train))
data_dev = x_train[500:800]
print("len data_dev: ",len(data_dev))
label_dev = y_train_np[500:800]
print("len label_dev: ",len(label_dev))
print("")

vectorizer = DictVectorizer()

X_train = vectorizer.fit_transform(data, label_train)
X_dev = vectorizer.transform(data_dev)

classifier = LogisticRegression()

classifier.fit(X_train, label_train)
print("classifier:\n",classifier)
print("")
predicted_y = classifier.predict(X_dev)
print("predicted_y: ",len(predicted_y),"\n",predicted_y)
print("")
print("accuracy_score:\n",accuracy_score(label_dev, predicted_y))
print("classification_report:\n",classification_report(label_dev, predicted_y))