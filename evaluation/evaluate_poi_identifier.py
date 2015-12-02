#!/usr/bin/python


"""
    starter code for the evaluation mini-project
    start by copying your trained/tested POI identifier from
    that you built in the validation mini-project

    the second step toward building your POI identifier!

    start by loading/formatting the data

"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn import cross_validation
data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=42)

### it's all yours from here forward!  

from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf.fit(features_train, labels_train)
predictions = clf.predict(features_test, labels_test)

num_predicted_poi = 0
for i in predictions:
    if i == 1:
        num_predicted_poi += 1
print(num_predicted_poi)
print(len(labels_test))

num_actual_poi = 0
for i in labels_test:
    if i == 1:
        num_actual_poi += 1
print("Number of actual PoI in test set: {}".format(num_actual_poi))
print("Accuracy if all 0: {}".format(float(num_actual_poi - 29)/29))

from sklearn import metrics
print(metrics.precision_score(labels_test, predictions))
print(metrics.recall_score(labels_test, predictions))


