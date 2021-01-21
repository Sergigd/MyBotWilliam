import numpy as np
from imblearn.over_sampling import SMOTE
from AI import AI_Methods as A_m
import time
import os
import pickle
import rootpath

# NeuralNet
from sklearn.neural_network import MLPClassifier
model_name = 'Neural'
type_model = 'NeuralNet'
model = MLPClassifier()

# # DecisionTree
# from sklearn.tree import DecisionTreeClassifier
# model_name = 'DT'
# type_model = 'DecisionTree'
# model = DecisionTreeClassifier()

# save params
vector_save = 'DB_Vectorizer.pkl'
name_save = model_name + '_v1' + '.pkl'


name_db = "english_db.db"  # "duplicated.db"
type_vector = 'Count'

time_start = time.time()
questions_db, y = A_m.load_questions_and_id(name_db)
X, vectorizer = A_m.get_x_and_vector(questions_db, type_vector)
yn = np.array(y)

print("Shape of X: ", X.shape)
print("Shape of y: ", yn.shape)

sm = SMOTE(sampling_strategy='all')
X_res, y_res = sm.fit_sample(X, yn)

print('After OverSampling, the shape of X_res: {}'.format(X_res.shape))
print('After OverSampling, the shape of y_res: {}'.format(y_res.shape))


model = model.fit(X_res, y_res)

if name_db == 'english_db.db':
    type_db = 'english_db'
elif name_db == 'duplicated.db':
    type_db = 'duplicated'
else:
    type_db = ""

root_dir = rootpath.detect()
path_vector = os.path.join(root_dir, 'AI', type_model, 'Vectorizer', "Smote", type_db, vector_save)
path_model = os.path.join(root_dir, 'AI', type_model, 'Models', "Smote", type_db, name_save)

pickle.dump(model, open(path_model, 'wb'))
pickle.dump(vectorizer, open(path_vector, 'wb'))

print("Model and vector saved")

time_finish = time.time()
print("Time = ", time_finish - time_start)
