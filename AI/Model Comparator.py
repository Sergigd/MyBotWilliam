import pickle
import os
from AI.Distance import Distance_Methods as nlp
from tensorflow import keras

# In this script we'll compare all the models in AI in order to check which model has more accuracy.

# Path_list
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path_AI = os.path.join(root_dir, "AI")

path_DT = os.path.join(path_AI, "DecisionTree", "Models")
path_NN = os.path.join(path_AI, "NeuralNet", "Models")
path_TFK = os.path.join(path_AI, "Tensorflow", "Models")

path_list = [path_DT, path_NN, path_NN]

# Loading Test Questions from Test_Similar_Questions.txt
questions_similar = nlp.read_questions_similar()

# Get the accuracy for each model: model, good, attempts
for path in path_list:
    # Files:
    models_list = os.listdir(path)
    models_accuracy = []

    if path.__contains__("DecisionTree"):
        folder = "DecisionTree"
    elif path.__contains__("NeuralNet"):
        folder = "NeuralNet"
    else:
        folder = "Tensorflow"

    for model in models_list:
        if model.__contains__("Count"):
            vector = os.path.join(path_AI, folder, "Vectorizer", "CountVectorizer.pkl")
        elif model.__contains__("Tfidf"):
            vector = os.path.join(path_AI, folder, "Vectorizer", "TFIDFVectorizer.pkl")
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
            title = questions_similar[predict_index[0] - 1]
            attempts += 1
            if question == title:
                good += 1

        models_accuracy.append([model_path, good, attempts])

index = 0
for num, models in enumerate(models_accuracy):
    # print("The model: {0} \nGood: {1}\nAttempts: {2}".format(models[0], models[1], models[2]))
    if models[1] > models_accuracy[index][1]:
        index = num

print("The model with most accuracy is: {0} \nGood: {1}\nAttempts: {2}".
      format(models_accuracy[index][0], models_accuracy[index][1], models_accuracy[index][2]))
