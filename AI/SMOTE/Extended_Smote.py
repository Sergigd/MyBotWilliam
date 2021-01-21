import numpy as np
from imblearn.over_sampling import SMOTE, RandomOverSampler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
import DataBase.DB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from AI import AI_Methods as A_m
from sklearn.model_selection import cross_val_score, train_test_split
import time
import os
import pickle
import rootpath

# # NeuralNet
# model_name = 'Neural'
# type_model = 'NeuralNet'
# model = MLPClassifier()

# DecisionTree
model_name = 'DT'
type_model = 'DecisionTree'
model = DecisionTreeClassifier()

# # Deep L.
# model_name = 'TF'
# type_model = 'Tensorflow'


# save params
vector_save = 'DB_Vectorizer.pkl'
name_save = model_name + '_v2' + '.pkl'


type_vector = 'Count'
name_db = "extended.db"

time_start = time.time()

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

print("Results: ,\n", results)

# Saving Count_Results.csv
header = vectorizer.get_feature_names()
header.append("Question_id")
results.to_csv(header=header, index=False)
results_id = results.pop("Question_id")

yn = np.array(vec_y)

# # Necessary to resample
X, X_test, y_train, y_test = train_test_split(results, yn, test_size=0.1, random_state=0)
#
# print("Number transactions X_train dataset: ", X_train.shape)
# print("Number transactions y_train dataset: ", y_train.shape)
# print("Number transactions X_test dataset: ", X_test.shape)
# print("Number transactions y_test dataset: ", y_test.shape)


sm = SMOTE(sampling_strategy='all')
X_res, y_res = sm.fit_sample(X, y)

model = model.fit(X_res, y_res)

# A_m.save_vector_and_model(vectorizer, model, model_name, type_vector, name_db)

if name_db == 'english_db.db':
    type_db = 'english_db'
elif name_db == 'duplicated.db':
    type_db = 'duplicated'
elif name_db == 'extended.db':
    type_db = 'extended'


root_dir = rootpath.detect()
path_vector = os.path.join(root_dir, 'AI', type_model, 'Vectorizer', "Smote", type_db, vector_save)
path_model = os.path.join(root_dir, 'AI', type_model, 'Models', "Smote", type_db, name_save)

pickle.dump(model, open(path_model, 'wb'))
pickle.dump(vectorizer, open(path_vector, 'wb'))

print("Model and vector saved")


time_finish = time.time()
print("Time = ", time_finish - time_start)
