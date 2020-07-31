import pickle
import os
from AI.NLP import NLP_Methods as nlp


# Files:
# Path
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path = os.path.join(root_dir, "AI", "DecisionTree")
# Count
file_model = os.path.join(path, "Models", "DT_Count_v2.pkl")
file_vector = os.path.join(path, "Vectorizer", "CountVectorizer.pkl")
# # TF-IDF
# file_model = os.path.join(path, "Models", "DT_Tfidf_v1.pkl")
# file_vector = os.path.join(path, "Vectorizer", "TFIDFVectorizer.pkl")


# Loading Test Questions from Test_Similar_Questions.txt
questions_similar = nlp.read_questions_similar()

# Loading Decision Tree Model
loaded_model = pickle.load(open(file_model, 'rb'))

# Loading CountVectorizer
vectorizer = pickle.load(open(file_vector, 'rb'))

# Test with questions
good = 0
attempts = 0
for question in questions_similar:
    question_x = vectorizer.transform([question])
    predict_index = loaded_model.predict(question_x)
    title = questions_similar[predict_index[0] - 1]
    attempts += 1
    if question == title:
        good += 1
    # print("Question: ", question)
    # print("Answer: ", title)

print("The model: {0} \nGood: {1}\nAttempts: {2}".format(file_model, good, attempts))
