# Methods of the AI
import rootpath
import os


def load_questions_and_id(name_db):
    import DataBase.DB
    data = DataBase.DB.MyData(name_db)
    # questions_and_id_db = data.get_repeated_q_and_id(30)
    questions_and_id_db = data.get_questions_and_id_db()

    questions_db = []
    y = []
    for question in questions_and_id_db:
        questions_db.append(question[0])
        y.append(question[1])
    return questions_db, y


def load_repeated_questions_and_id(name_db, number):
    import DataBase.DB
    data = DataBase.DB.MyData(name_db)
    questions_and_id_db = data.get_repeated_q_and_id(number)

    questions_db = []
    y = []
    for question in questions_and_id_db:
        questions_db.append(question[0])
        y.append(question[1])
    return questions_db, y


def get_x_and_vector(questions_db, type_vectorizer='Count'):
    if type_vectorizer == 'Count':
        # Counting
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
        x = vectorizer.fit_transform(questions_db)
        return x, vectorizer
    else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
        x = vectorizer.fit_transform(questions_db)
        return x, vectorizer


def train_sk_model(x, y, type_model='Tree'):
    if type_model == 'Tree':
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier()
    else:
        from sklearn.neural_network import MLPClassifier
        model = MLPClassifier()

    model = model.fit(x, y)
    return model


def train_tensor_model(x, y, total_layers=2, first_dim_layer=1):
    # Check the optional inputs format
    if type(total_layers) is not int or type(first_dim_layer) is not int:
        print("Bad format.")
        return -1

    from tensorflow import keras
    from tensorflow.keras.layers import Dense
    import numpy as np

    # Prepare outputs: a binary class matrix
    output_y = keras.utils.to_categorical(y)

    # Get shape of vectors
    shape_y = np.shape(output_y)[1]
    shape_x = np.shape(x)[1]
    dimensional_step = int((shape_y - first_dim_layer) / total_layers)
    theoretically_last_layer = dimensional_step * total_layers + first_dim_layer

    # Checks
    if total_layers < 2:
        print("Minimum layers = 2")
        return -1
    elif total_layers > shape_y:
        print("Too many layers: there are more layers than questions.")
        # shape_y cannot be lower than the number of layers
        return -1
    elif first_dim_layer >= shape_y:
        print("The dimension of the first layer should be lower than the questions")
        # first_dim_layer cannot be greater than the number of ids.
        return -1
    elif dimensional_step <= 0:
        print("Too many layers for the dimensions we have")
        return -1

    # Create the model
    model = keras.models.Sequential()
    model.add(Dense(first_dim_layer, input_dim=shape_x, activation='relu'))
    # from tensorflow.keras.layers import Dropout
    # model.add(Dropout(.2))

    for dim in range(first_dim_layer + dimensional_step, theoretically_last_layer - dimensional_step, dimensional_step):
        model.add(Dense(dim, activation='relu'))

    model.add(Dense(shape_y, activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(x, output_y, epochs=150, batch_size=15, verbose=1)

    root_dir = rootpath.detect()
    # name = "TFKeras_Count_Dropout" + str(total_layers) + "-" + str(first_dim_layer) + ".pkl"
    name = "TFKeras_Count_" + str(total_layers) + "-" + str(first_dim_layer) + ".pkl"
    path_model = os.path.join(root_dir, "AI", "Tensorflow", "Models", "Smote", "extended", name)

    model.save(path_model)

    return model, name


def save_vector_and_model(vectorizer, model, model_name, type_vector, name_db):
    if model_name == 'Tree' or model_name == 'DT':
        type_model = 'DecisionTree'
        model_short = 'DT'
    elif model_name == 'Neural' or model_name == 'NN':
        type_model = 'NeuralNet'
        model_short = 'Neural'
    elif model_name == 'TF' or model_name == 'Keras':
        type_model = 'Tensorflow'
        model_short = 'TFKeras'
    else:
        print("Model incorrect.")
        return -1

    if name_db == 'first_db.db':
        type_db = 'first_db'
    elif name_db == 'english_db.db':
        type_db = 'english_db'
    elif name_db == 'duplicated.db':
        type_db = 'duplicated'
    elif name_db == 'extended.db':
        type_db = 'extended'
    else:
        print("No folder for this DataBase")
        return -1

    if type_vector == 'Count':
        vector = 'DB_Vectorizer.pkl'
    elif type_vector == 'tfidf':
        vector = 'TFIDFVectorizer.pkl'
    else:
        print("No type_vector")
        return -1

    root_dir = rootpath.detect()
    path_vector = os.path.join(root_dir, 'AI', type_model, 'Vectorizer', type_db, vector)
    path_model = get_path_model(root_dir, type_model, model_short, type_db, type_vector)

    import pickle
    if model_short == 'TFKeras':
        model.save(path_model)
    else:
        pickle.dump(model, open(path_model, 'wb'))

    pickle.dump(vectorizer, open(path_vector, 'wb'))

    print("Model and vector saved")
    return 0


def get_path_model(root_dir, type_model, model_short, type_db, type_vector):
    path = os.path.join(root_dir, 'AI', type_model, 'Models', type_db)
    print(path)
    models_list = os.listdir(path)
    models = [model for model in models_list if model.__contains__(type_vector)]

    model_version = len(models) + 1
    if model_short == 'TF':
        model_name = model_short + '_' + type_vector + '_v' + str(model_version) + '.h5'

    else:
        model_name = model_short + '_' + type_vector + '_v' + str(model_version) + '.pkl'
    return os.path.join(path, model_name)
