import pandas as pd
import numpy as np
import os

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from matplotlib import pyplot
from sklearn.datasets import make_classification
from collections import Counter
from numpy import where
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold
from sklearn.tree import DecisionTreeClassifier
import DataBase.DB
from sklearn.model_selection import cross_val_score
from numpy import mean


# --------------------------------------------------------
# https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/
# from numpy import mean
# from sklearn.datasets import make_classification
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import RepeatedStratifiedKFold
# from sklearn.tree import DecisionTreeClassifier
#
# # define dataset
# X, y = make_classification(n_samples=10000, n_features=2, n_redundant=0,
#                            n_clusters_per_class=1, weights=[0.99], flip_y=0, random_state=1)
# # values to evaluate
# k_values = [1, 2, 3, 4, 5, 6, 7]
# for k in k_values:
#     # define pipeline
#     model = DecisionTreeClassifier()
#     over = SMOTE(sampling_strategy=0.1, k_neighbors=k)
#     under = RandomUnderSampler(sampling_strategy=0.5)
#     steps = [('over', over), ('under', under), ('model', model)]
#     pipeline = Pipeline(steps=steps)
#     # evaluate pipeline
#     cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
#     scores = cross_val_score(pipeline, X, y, scoring='roc_auc', cv=cv, n_jobs=-1)
#     score = mean(scores)
#     print('> k=%d, Mean ROC AUC: %.3f' % (k, score))
# --------------------------------------------------------
#
#
# In this script we will generate different Decision Trees Models.

# Load questions from DB
data = DataBase.DB.MyData("english_db.db")
questions_and_id_db = data.get_questions_and_id_dB()

questions_db = []
y = []
for question in questions_and_id_db:
    questions_db.append(question[0])
    y.append(question[1])

# Counting
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
X = vectorizer.fit_transform(questions_db)

# # # Saving CountVectorizer
# import pickle
# filename = "/DecisionTree/Vectorizer/CountVectorizer.pkl"
# pickle.dump(vectorizer, open(filename, 'wb'))

results = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
results['Question_id'] = y  # Concatenate X and y

o = np.array(y)
unique, counts = np.unique(o, return_counts=True)
print("X :", X)
print("y 1: ", y)
print("Unique 1: ", unique)
print("Counts 1: ", counts)

# Reshape using SMOTE
k_values = [1, 2, 3, 4, 5, 6, 7]

# for k in k_values:
    # define pipeline
model = DecisionTreeClassifier()
overSample = SMOTE(sampling_strategy='all')
    # for _ in k_values:
        # steps = [('over', over), ('model', model)]
X_, y_ = overSample.fit_resample(X, y)

        # pipeline = Pipeline(steps=steps)
    # evaluate pipeline
cv = RepeatedStratifiedKFold(n_splits=3, n_repeats=3, random_state=1)
scores = cross_val_score(model, X_, y_, scoring='roc_auc', cv=cv, n_jobs=-1)
score = mean(scores)
print('Mean ROC AUC: %.3f' % (score))
#
# # Saving Count_Results.csv
# root_dir = os.path.dirname(os.path.abspath(os.curdir))
# path = os.path.join(root_dir, "AI", "DecisionTree", "CSV_Results", "Count_Results.csv")
# header = vectorizer.get_feature_names()
# header.append("Question_id")
# results.to_csv(path_or_buf=path, header=header, index=False)
# results_id = results.pop("Question_id")

# p = np.array(y)
# unique, counts = np.unique(p, return_counts=True)
# print("X :", X)
# print("y 2: ", y)
# print("Unique 2: ", unique)
# print("Counts 2: ", counts)
#
# # Computing cross-validated metrics
# from sklearn.model_selection import cross_val_score
#
# clf = DecisionTreeClassifier()
# scores = cross_val_score(clf, X, y, cv=2)
# print(scores)


print(type(X_))
print(type(X))
print(type(y))
print(type(y_))
