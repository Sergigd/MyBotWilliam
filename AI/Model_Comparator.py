import pickle
import os
from AI.Distance import Distance_Methods as Nlp
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import *

# In this script we'll compare all the models in AI in order to check which model has more accuracy.
type_db = "First_DataBase"

# Path_list
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path_AI = os.path.join(root_dir, "AI")

path_DT = os.path.join(path_AI, "DecisionTree", "Models", type_db)
path_NN = os.path.join(path_AI, "NeuralNet", "Models", type_db)
path_TFK = os.path.join(path_AI, "Tensorflow", "Models", type_db)

path_list = [path_DT, path_NN, path_TFK]

# Loading Test Questions from Test_Similar_Questions.txt
questions_similar = Nlp.read_questions_similar()

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
            question_x = vectorizer.transform([question])
            predict_index = loaded_model.predict(question_x)
            if folder == "Tensorflow":
                max_predict = max(predict_index[0])
                for index, value in enumerate(predict_index[0]):
                    if value == max_predict:
                        break
                title = questions_similar[index - 1]
            else:
                title = questions_similar[predict_index[0] - 1]
            attempts += 1
            if question == title:
                good += 1

        # Save model_name, good, attempts, accuracy
        accuracy = good/attempts
        model_name = model_path.replace(path_AI, "", -1).replace("\\Models\\First_DataBase\\", "", -1)\
            .replace("\\", "", -1).replace("DecisionTree", "", -1).replace("NeuralNet", "", -1).replace(".pkl", "", -1)\
            .replace("Tensorflow", "", -1)
        model_good_att_acc.append([model_name, good, attempts, accuracy*100])

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
