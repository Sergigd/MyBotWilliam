import DataBase.DB
from AI import AI_Methods as A_m
import time

model_name = 'TF'
type_vector = 'Count'
# type_vector = 'tfidf'
name_db = "first_db.db"
# # Load questions from DB
time_start = time.time()

data = DataBase.DB.MyData("first_db.db")

questions_db, y = A_m.load_questions_and_id(name_db)

X, vectorizer = A_m.get_x_and_vector(questions_db, type_vector)

model = A_m.train_tensor_model(X, y, total_layers=2, first_dim_layer=20)
if model == -1:
    print("Quit")
    quit()

A_m.save_vector_and_model(vectorizer, model, model_name, type_vector, name_db)

time_finish = time.time()

print("Time = ", time_finish - time_start)
#
# # Evaluate the model
# score = model.evaluate(X, output_y, batch_size=15)

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
#
# print("Value = ", value)
# print("Index = ", index)
print("Text = ", text[0])
title = data.get_title_by_id(index)[0]
print("Result = ", title)


# # Saving model
# yes_no = input('Save?:')
# if yes_no == 'y':
