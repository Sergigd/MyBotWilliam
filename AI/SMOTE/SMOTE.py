import pandas as pd
import numpy as np
import os
from collections import Counter
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
import DataBase.DB
from sklearn.model_selection import cross_val_score
from numpy import mean


# Load questions from DB
data = DataBase.DB.MyData("english_db.db")
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

# Original input
o = np.array(y)
unique, counts = np.unique(o, return_counts=True)
print("X :", X)
print("y: ", y)
print("Unique 1: ", unique)
print("Counts 1: ", counts)

# Reshape using SMOTE
overSample = SMOTE(sampling_strategy='all')
X_, y_ = overSample.fit_resample(X, y)

# SMOTE output
o = np.array(y_)
unique, counts = np.unique(o, return_counts=True)
print("X_ :", X_)
print("y_: ", y_)
print("Unique 2: ", unique)
print("Counts 2: ", counts)

clf = DecisionTreeClassifier()
clf.fit(X_, y_)


# Test
# Calling the base constructor in C#
text = ["call the constructor"]
test = vectorizer.transform(text)
test2 = clf.predict(test)
print(test)
print(test2)
index_y = y[test2[0] - 1]
print(index_y)
title = data.get_title_by_id(index_y)
print(title[0])
