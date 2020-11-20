import pickle
import os
from AI.Distance import Distance_Methods as nlp
from tensorflow import keras


# Files:
# Path
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path = os.path.join(root_dir, "Tensorflow")
# Count
file_model = os.path.join(path, "Models", "First_DataBase", "TFKeras_Count_v3.h5")
file_vector = os.path.join(path, "Vectorizer", "CountVectorizer.pkl")
# # TF-IDF
# file_model = os.path.join(path, "Models", "DT_Tfidf_v1.pkl")
# file_vector = os.path.join(path, "Vectorizer", "TFIDFVectorizer.pkl")


# Loading Test Questions from Test_Similar_Questions.txt
questions_similar = nlp.read_questions_similar()

# Loading Keras
loaded_model = keras.models.load_model(file_model)
# loaded_model = pickle.load(open(file_model, 'rb'))

# Loading CountVectorizer
vectorizer = pickle.load(open(file_vector, 'rb'))

# Test with questions
good = 0
attempts = 0
for question in questions_similar:
    question_x = vectorizer.transform([question])
    predict_model = loaded_model.predict(question_x)
    max_predict = max(predict_model[0])
    for index, value in enumerate(predict_model[0]):
        if value == max_predict:
            break

    title = questions_similar[index - 1]
    attempts += 1
    if question == title:
        good += 1
    # print("Question: ", question)
    # print("Answer: ", title)

print("The model: {0} \nGood: {1}\nAttempts: {2}".format(file_model, good, attempts))
