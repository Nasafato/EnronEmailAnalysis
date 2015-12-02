#!/usr/bin/python

""" 
    this is the code to accompany the Lesson 2 (SVM) mini-project

    use an SVM to identify emails from the Enron corpus by their authors
    
    Sara has label 0
    Chris has label 1

"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import numpy as np
clf = SVC(C=10000.0, kernel="rbf")

# these two lines takes 1% of the original data instead
# features_train = features_train[:len(features_train)/100] 
# labels_train = labels_train[:len(labels_train)/100] 

t0 = time()
clf.fit(features_train, labels_train)
print("training time: {} s".format(round(time() - t0, 3)))

t1 = time()
pred = clf.predict(features_test)
print("prediction time: {} s".format(round(time() - t1, 3)))

print(accuracy_score(labels_test, pred))
print("Number of predictions with Chris: {}".format(np.count_nonzero(pred)))
# print("10: {}, 26: {}, 50: {}".format(pred[10], pred[26], pred[50]))

#########################################################


