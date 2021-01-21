from AI import AI_Methods as A_m
import time

# In this script we will generate different NeuralNet Models.
model_name = 'Neural'
type_vector = 'Count'
name_db = "duplicated.db"  # "english_db.db", "first_db.db"

time_start = time.time()

questions_db, y = A_m.load_questions_and_id(name_db)

X, vectorizer = A_m.get_x_and_vector(questions_db, type_vector)

model = A_m.train_sk_model(X, y, vectorizer)

A_m.save_vector_and_model(vectorizer, model, model_name, type_vector, name_db)
time_finish = time.time()

print("Time = ", time_finish - time_start)
