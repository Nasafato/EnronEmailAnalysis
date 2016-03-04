#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

import pprint

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest, f_classif

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### list the features you want to look at--first item in the
### list will be the "target" feature

target_label = [
    'poi'
]

financial_features = [
     'salary',
     'deferral_payments',
     'total_payments',
     'exercised_stock_options',
     'bonus',
     'restricted_stock',
     'shared_receipt_with_poi',
     'restricted_stock_deferred',
     'total_stock_value',
     'expenses',
     'loan_advances',
     'other',
     'director_fees',
     'deferred_income',
     'long_term_incentive',
]

email_features = [
    'from_messages',
    'to_messages',
    'from_poi_to_this_person',
    'from_this_person_to_poi',
    'shared_receipt_with_poi'
]

outliers = [
    'TOTAL',
    'THE TRAVEL AGENCY IN THE PARK',
]

# remove outliers from the data
for outlier_key in outliers:
    del data_dict[outlier_key]

features_list = target_label + financial_features + email_features
data = featureFormat(data_dict, features_list)
target, features = targetFeatureSplit( data )

# get 10 best features
selector = SelectKBest(k=10)
selector.fit(features, target)
feature_names = [features_list[i] for i in selector.get_support(indices=True)]
features_list = target_label + feature_names

# poi_message_ratios - ratio of poi messages to total messages
for name in data_dict:
    try:
        total_messages = data_dict[name]['from_messages'] + data_dict[name]['to_messages']
        poi_messages = data_dict[name]['from_poi_to_this_person'] +\
                       data_dict[name]['from_this_person_to_poi'] +\
                       data_dict[name]['shared_receipt_with_poi']

        data_dict[name]['poi_message_ratio'] = (float)(poi_messages/total_messages)
    except (TypeError, KeyError):
        data_dict[name]['poi_message_ratio'] = 'NaN'

features_list.append('poi_message_ratio')

### Store to my_dataset for easy export below.
my_features_list = features_list
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, my_features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# scale the features
from sklearn import preprocessing
scaler = preprocessing.MinMaxScaler()
features = scaler.fit_transform(features)

# create classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

nb_clf = GaussianNB()
log_clf = LogisticRegression(C=10**18, tol=10**-21)
kmeans_clf = KMeans(n_clusters=3, tol=0.001)
rf_clf = RandomForestClassifier()

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

log_clf.fit(features_train, labels_train)
predictions = log_clf.predict(features_test)

print(accuracy_score(labels_test, predictions))
print(precision_score(labels_test, predictions))
print(recall_score(labels_test, predictions))

clf = log_clf

dump_classifier_and_data(clf, my_dataset, features_list)