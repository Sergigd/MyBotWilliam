from AI import AI_Methods as A_m
import time

# In this script we will generate different Decision Trees Models.
model_name = 'DT'
type_vector = 'Count'
name_db = "duplicated.db"  # "english_db.db", "first_db.db"

time_start = time.time()

if name_db == 'duplicated.db':
    questions_db, y = A_m.load_repeated_questions_and_id(name_db, 30)
else:
    questions_db, y = A_m.load_questions_and_id(name_db)

X, vectorizer = A_m.get_x_and_vector(questions_db, type_vector)

model = A_m.train_sk_model(X, y)

A_m.save_vector_and_model(vectorizer, model, model_name, type_vector, name_db)
time_finish = time.time()

print("Total time = ", time_finish - time_start)
