import pickle
import time
from AI.Distance import Distance_Methods as Nlp
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import *
from DataBase.DB import MyData
import tensorflow as tf


# In this script we'll compare the models in Tensorflow in order to check which model has more accuracy.

type_db = "english_db"  # english_db.db, first_db.db
db = MyData(type_db + ".db")

# Avoid Warnings of Tensorflow
tf.get_logger().setLevel('INFO')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}

# Path_list
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path_AI = os.path.join(root_dir)
path_TFK = os.path.join(path_AI, "Tensorflow", "Models", type_db)

path_list = [path_TFK]

# Loading Test Questions from Test_Similar_Questions.txt
# questions_similar = Nlp.read_questions_similar()
questions_similar = Nlp.read_questions_similar_with_check()

# Get the accuracy for each model: model, good, attempts, accuracy
model_good_att_acc = []
for path in path_list:
    # Files:
    models_list = os.listdir(path)

    if path.__contains__("DecisionTree"):
        folder = "DecisionTree"
    elif path.__contains__("NeuralNet"):
        folder = "NeuralNet"
    else:
        folder = "Tensorflow"

    for model in models_list:
        if model.__contains__("Count"):
            vector = os.path.join(path_AI, folder, "Vectorizer", type_db, "CountVectorizer.pkl")
        elif model.__contains__("Tfidf"):
            vector = os.path.join(path_AI, folder, "Vectorizer", type_db, "TFIDFVectorizer.pkl")
        else:
            print(model)
            print("Break")
            break
        time_start = time.time()

        # Loading model
        model_path = os.path.join(path, model)
        if folder == "Tensorflow":
            loaded_model = keras.models.load_model(model_path)
        else:
            loaded_model = pickle.load(open(model_path, 'rb'))

        # Loading CountVectorizer
        vectorizer = pickle.load(open(vector, 'rb'))

        # Test with questions
        good = 0
        attempts = 0
        for question in questions_similar:
            question_x = vectorizer.transform([question[0]])
            predict_index = loaded_model.predict(question_x)
            index = ""
            if folder == "Tensorflow":
                max_predict = max(predict_index[0])
                for index, value in enumerate(predict_index[0]):
                    if value == max_predict:
                        break
                title_db = db.get_title_by_id(index)[0]
            else:
                title_db = db.get_title_by_id(int(predict_index[0]))[0]
            attempts += 1
            if question[1] == str(title_db).lower():
                good += 1
        time_finish = time.time()
        time_model = time_finish - time_start

        # Save model_name, good, attempts, accuracy
        accuracy = good/attempts
        model_name = model_path.replace(path_AI, "", -1).replace("\\Models\\" + type_db + "\\", "", -1)\
            .replace("\\", "", -1).replace("DecisionTree", "", -1).replace("NeuralNet", "", -1).replace(".pkl", "", -1)\
            .replace("Tensorflow", "", -1).replace("TFKeras_Count_", "", -1)
        model_good_att_acc.append([model_name, good, attempts, accuracy*100])
        print(model_name, ": time = ", time_model, " Good = ", good, " accuracy = ", accuracy)

# Which is the model with most accuracy
index = [0]
for num, models in enumerate(model_good_att_acc):
    if models[3] > model_good_att_acc[index[0]][3]:
        index = [num]
    elif models[3] == model_good_att_acc[index[0]][3]:
        index.append(num)

for num in index:
    print("The model/s with most accuracy is/are: {0} \nGood: {1}\nAttempts: {2}\nAccuracy: {3}\n".
          format(model_good_att_acc[num][0], model_good_att_acc[num][1],
                 model_good_att_acc[num][2], model_good_att_acc[num][3]))


# Plot
models = np.array(model_good_att_acc)[:, 0]
accuracy = np.array(model_good_att_acc)[:, 3].astype(np.float)

fig, ax = plt.subplots()
plt.bar(models, accuracy)

ax.set_ylabel('Accuracy (%)')
ax.set_title('Accuracy of the Models')
plt.xticks(rotation=25)
plt.ylim(0, 100)

plt.show()
