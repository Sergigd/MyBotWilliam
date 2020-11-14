from tensorflow import keras
from tensorflow.keras.layers import Dense
import DataBase.DB


# Load questions from DB
data = DataBase.DB.MyData()
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

# Saving CountVectorizer
import pickle
filename = "Vectorizer/CountVectorizer.pkl"
pickle.dump(vectorizer, open(filename, 'wb'))

# Prepare outputs: a binary class matrix
output_y = keras.utils.to_categorical(y)  # (results_id, 30)?

# Create the model
model = keras.models.Sequential()
model.add(Dense(8, input_dim=95, activation='relu'))
model.add(Dense(31, activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, output_y, epochs=150, batch_size=15, verbose=1)

# Evaluate the model
score = model.evaluate(X, output_y, batch_size=15)

# Test
text = ["how to merge"]
transform = vectorizer.transform(text)
test = model.predict(transform)
print(test)

max_test = max(test[0])
print(max_test)
for index, value in enumerate(test[0]):
    if value == max_test:
        break

print("Value = ", value)
print("Index = ", index)
print("Text = ", text[0])
title = data.get_title_by_id(index)[0]
print("Result = ", title)


# Saving model
yes_no = input('Save?:')
if yes_no == 'y':
    model.save("Models/TFKeras_Count_v3.h5")
