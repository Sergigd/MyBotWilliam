# Methods of the AI
import rootpath
import os


def load_questions_and_id(name_db):
    import DataBase.DB
    data = DataBase.DB.MyData(name_db)
    questions_and_id_db = data.get_questions_and_id_dB()

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
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=42)

    if type_model == 'Tree':
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier()
    else:
        from sklearn.neural_network import MLPClassifier
        model = MLPClassifier()

    model = model.fit(x_train, y_train)
    return model


def train_tensor_model(x, y, total_layers=2, first_dim_layer=1):
    # Check the optional inputs format
    if total_layers is not int or first_dim_layer is not int:
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

    for dim in range(first_dim_layer, shape_y, dimensional_step):
        model.add(Dense(dim, activation='relu'))

    model.add(Dense(shape_y, activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(x, output_y, epochs=150, batch_size=15, verbose=1)
    return model


def save_vector_and_model(vectorizer, model, model_name, type_vector, name_db):
    if model_name == 'Tree' or 'DT':
        type_model = 'DecisionTree'
        model_short = 'DT'
    elif model_name == 'Neural' or model == 'NN':
        type_model = 'NeuralNet'
        model_short = 'Neural'
    else:
        print("Model incorrect.")
        return -1

    if name_db == 'first_db.db':
        type_db = 'First_DataBase'
    elif model == 'english_db.db':
        type_db = 'Extended_DataBase'
    else:
        print("No folder for this DataBase")
        return -1

    if type_vector == 'Count':
        vector = 'CountVectorizer.pkl'
    elif type_vector == 'tfidf':
        vector = 'TFIDFVectorizer.pkl'
    else:
        print("No type_vector")
        return -1

    root_dir = rootpath.detect()
    path_vector = os.path.join(root_dir, 'AI', type_model, 'Vectorizer', type_db, vector)
    path_model = get_path_model(root_dir, type_model, model_short, type_db, type_vector)

    import pickle
    pickle.dump(vectorizer, open(path_vector, 'wb'))
    pickle.dump(model, open(path_model, 'wb'))

    print("Model and vector saved")
    return 0


def get_path_model(root_dir, type_model, model_short, type_db, type_vector):
    path = os.path.join(root_dir, 'AI', type_model, 'Models', type_db)
    print(path)
    models_list = os.listdir(path)
    models = [model for model in models_list if model.__contains__(type_vector)]

    model_version = len(models) + 1
    model_name = model_short + '_' + type_vector + '_v' + str(model_version) + '.pkl'
    return os.path.join(path, model_name)
