import pandas as pd
import numpy as np
import os
from collections import Counter
from imblearn.over_sampling import SMOTE
from AI.Distance import Distance_Methods as DM
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

#
# # --------------------------------------------------------
# # https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/
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
# # --------------------------------------------------------

# Load questions from DB
data = DataBase.DB.MyData("english_DB.db")
questions_and_id_db = data.get_questions_and_id_dB()

questions_db = []
y = []
for num, question in enumerate(questions_and_id_db):
    questions_db.append(question[0])

    y.append(question[1])

print(questions_db[0])
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
print("y: ", y)
print("Unique 1: ", unique)
print("Counts 1: ", counts)

# Reshape using SMOTE
k_values = [1, 2, 3, 4, 5, 6, 7]

# for k in k_values:
    # define pipeline

overSample = SMOTE(sampling_strategy='all')
    # for _ in k_values:
        # steps = [('over', over), ('model', model)]
X_, y_ = overSample.fit_resample(X, y)

o = np.array(y_)
unique, counts = np.unique(o, return_counts=True)

print("X_ :", X_)
print("y 2: ", y_)
print("Unique 2: ", unique)
print("Counts 2: ", counts)

clf = DecisionTreeClassifier()
clf.fit(X_, y_)

# Test Calling the base constructor in C#
text = ["constructor"]
test = vectorizer.transform(text)
test2 = clf.predict(test)
print(test)
print(test2)
index_y = y[test2[0] - 1]
print(index_y)
title = data.get_title_by_id(index_y)
print(title[0])
