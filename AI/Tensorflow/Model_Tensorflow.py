from sklearn import datasets
from tensorflow import keras
from tensorflow.keras.layers import Dense
import pandas as pd
import DataBase.DataSource

# 1) import data
# Load questions from DB
data = DataBase.DataSource.data()
questions_and_id_db = data.get_questions_and_id_dB()

questions_db = []
y = []
for question in questions_and_id_db:
    questions_db.append(question[0])
    y.append(question[1])

# print(questions_db)
# print(y)

iris = datasets.load_iris()
# print("iris:")
# print(iris)
#
# # 2) prepare inputs
# input_x = iris.data
#
# # 3) prepare outputs: a binary class matrix
#
# # output_y = keras.utils.to_categorical(iris.target, 3)
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
X = vectorizer.fit_transform(questions_db)
# import pickle
# filename = "Vectorizer/CountVectorizer.pkl"
# pickle.dump(vectorizer, open(filename, 'wb'))

results = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
# results['Question_id'] = y  # Concatenate X and y

# print("data")
# print(iris.data)
# print("Vectorizer")
# print(vectorizer.get_feature_names())
# print("Results")
# print(results)
# results_id = results.pop("Question_id")
results_id = y

output_y = keras.utils.to_categorical(results_id)  # (results_id, 30)?

# 4a) Create the model
model = keras.models.Sequential()
model.add(Dense(8, input_dim=95, activation='relu'))
model.add(Dense(31, activation='softmax'))

# 4b) Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 4c) Fit the model
model.fit(X, output_y, epochs=150, batch_size=15, verbose=1)

# 4d) Evaluate the model
score = model.evaluate(X, output_y, batch_size=15)
# score

# Test
text = vectorizer.transform(["how to merge"])
test = model.predict(text)
print(test)

max_test = max(test[0])
print(max_test)
for index, value in enumerate(test[0]):
    if value == max_test:
        break

print("Value = ", value)
print("Index = ", index)
print("Text = ", text)
title = data.get_title_by_id(index)
print("Result = ", title)
