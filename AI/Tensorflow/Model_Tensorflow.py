from AI import AI_Methods as A_m
import time

# parameters
model_name = 'TF'
type_vector = 'Count'
name_db = "duplicated.db"  # english_db.db, first_db.db

# timer
time_start = time.time()

if name_db == 'duplicated.db':
    questions_db, y = A_m.load_repeated_questions_and_id(name_db, 30)
else:
    questions_db, y = A_m.load_questions_and_id(name_db)

X, vectorizer = A_m.get_x_and_vector(questions_db, type_vector)


layers = [2]
dimensions = [250]
for layer in layers:
    print("Layer = ", layer)
    for dim in dimensions:
        print("Dim = ", dim)
        time_start_model = time.time()
        model, name = A_m.train_tensor_model(X, y, total_layers=layer, first_dim_layer=dim)
        time_finish_model = time.time()
        total_time = time_finish_model - time_start_model
        print("TIME= ", total_time)

time_finish = time.time()

print("Time = ", time_finish - time_start)
