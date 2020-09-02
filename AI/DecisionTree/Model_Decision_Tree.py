import pandas as pd
import os
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import DataBase.DataSource
import numpy as np

# In this script we will generate different Decision Trees Models.

# Load questions from DB
data = DataBase.DataSource.data()
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

# # Saving CountVectorizer
import pickle
filename = "/DecisionTree/Vectorizer/CountVectorizer.pkl"
pickle.dump(vectorizer, open(filename, 'wb'))

results = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
results['Question_id'] = y  # Concatenate X and y

# Saving Count_Results.csv
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path = os.path.join(root_dir, "AI", "DecisionTree", "CSV_Results", "Count_Results.csv")
header = vectorizer.get_feature_names()
header.append("Question_id")
results.to_csv(path_or_buf=path, header=header, index=False)
results_id = results.pop("Question_id")


# TFIDF
# from sklearn.feature_extraction.text import TfidfVectorizer
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(questions_db)
#
# # Saving TFIDFVectorizer
# import pickle
# filename = "DecisionTree/Vectorizer/TFIDFVectorizer.pkl"
# pickle.dump(vectorizer, open(filename, 'wb'))
#
# results = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
# results['Question_id'] = y  # Concatenate X and y
#
# # Saving TFIDF_Results.csv
# root_dir = os.path.dirname(os.path.abspath(os.curdir))
# path = os.path.join(root_dir, "AI", "DecisionTree", "CSV_Results", "TFIDF_Results.csv")
# header = vectorizer.get_feature_names()
# header.append("Question_id")
# results.to_csv(path_or_buf=path, header=header, index=False)
# results_id = results.pop("Question_id")-

# DecisionTreeClassifier()
X_train, X_test, y_train, y_test = train_test_split(results, results_id, test_size=0.4, random_state=42)
clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
score = clf.score(X_test, y_test)
print("Score: ", score)
# Print model.results
from sklearn import tree
from matplotlib import pyplot as plt
tree.plot_tree(clf, filled=True)
plt.show()

# Saving model
yes_no = input('Save?:')
if yes_no == 'y':
    # Save to file in the current working directory
    import pickle
    filename = "Models/DT_Count_v5.pkl"
    pickle.dump(clf, open(filename, 'wb'))

# Test
text = ["javascript"]
test = vectorizer.transform(text)
test2 = clf.predict(test)
print(test)
print(test2)
index_y = y[test2[0] - 1]
print(index_y)
title = data.get_title_by_id(index_y)
print(title)


# https://stackoverflow.com/questions/44193154/notfittederror-tfidfvectorizer-vocabulary-wasnt-fitted
