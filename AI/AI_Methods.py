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


def train_model(x, y, vectorizer, type_model='Tree'):
    import pandas as pd
    results = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())
    results['Question_id'] = y  # Concatenate X and y

    header = vectorizer.get_feature_names()
    header.append("Question_id")
    results_id = results.pop("Question_id")

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(results, results_id, test_size=0.4, random_state=42)

    if type_model == 'Tree':
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier()
    else:
        from sklearn.neural_network import MLPClassifier
        model = MLPClassifier()

    model = model.fit(x_train, y_train)
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
    # filename = "Vectorizer/CountVectorizer.pkl"
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
