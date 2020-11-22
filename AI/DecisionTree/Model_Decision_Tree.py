import DataBase.DB
from AI import AI_Methods as A_m
import time

# In this script we will generate different Decision Trees Models.
model_name = 'DT'
type_vector = 'Count'
# type_vector = 'tfidf'
name_db = "first_db.db"

time_start = time.time()
# # Load questions from DB
data = DataBase.DB.MyData("first_db.db")

questions_db, y = A_m.load_questions_and_id(name_db)

X, vectorizer = A_m.get_x_and_vector(questions_db, type_vector)

model = A_m.train_sk_model(X, y, vectorizer)

A_m.save_vector_and_model(vectorizer, model, model_name, type_vector, name_db)
time_finish = time.time()

print("Time = ", time_finish - time_start)
# Test
text = ["merge in GitHub?"]
test = vectorizer.transform(text)
test2 = model.predict(test)
print(test)
print(test2)
index_y = y[test2[0] - 1]
print(index_y)
title = data.get_title_by_id(index_y)
print(title)



