import DataBase.DB
from sklearn.feature_extraction.text import CountVectorizer
from AI import AI_Methods as A_m
import time
import pandas as pd
import os

# In this script we will generate different Decision Trees Models.
model_name = 'DT'
type_vector = 'Count'
name_db = "extended.db"  # duplicated.db, english_db.db

# start timer
time_start = time.time()

# Load questions from DB
data = DataBase.DB.MyData(name_db)
questions_and_id_db = data.get_questions_extended_id_db()

questions_db = []
extended_q = []
vec = []
vec_y = []
y = []
for question in questions_and_id_db:
    questions_db.append(question[0])
    extended_q.append(question[1])
    vec.append(question[0])
    vec.append(question[1])
    vec_y.append(question[2])
    vec_y.append(question[2])
    y.append(question[2])


# Counting
vectorizer = CountVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
x = vectorizer.fit_transform(vec)
results = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())
results['Question_id'] = vec_y  # Concatenate X and y

# Saving Count_Results.csv
header = vectorizer.get_feature_names()
header.append("Question_id")
results.to_csv(header=header, index=False)
results_id = results.pop("Question_id")

# from sklearn.tree import DecisionTreeClassifier
# model = DecisionTreeClassifier()
# model.fit(results, vec_y)
# A_m.save_vector_and_model(vectorizer, model, model_name, type_vector, name_db)

layers = [2]
dimensions = [250]
for layer in layers:
    print("Layer = ", layer)
    for dim in dimensions:
        print("Dim = ", dim)
        time_start_model = time.time()
        model, name = A_m.train_tensor_model(results, vec_y, total_layers=layer, first_dim_layer=dim)
        time_finish_model = time.time()
        total_time = time_finish_model - time_start_model
        print("TIME  ", total_time)


time_finish = time.time()
print("Time = ", time_finish - time_start)
