"""
This is MyBotWilliam, a chatbot for solving programming questions. It works with a Neural Net model and a Database
generated with the API of Stackoverflow.
"""
import pickle
from AI.Distance.Distance_Methods import prepare_sentence, cosine_similarity
from DataBase.DB import MyData


def william_response(input_question):
    prepared_question = prepare_sentence(input_question)
    path_model = r"William_NN.pkl"
    path_vector = r"DB_Vectorizer.pkl"

    # Load model, Vectorizer and DataBase
    model = pickle.load(open(path_model, 'rb'))
    vectorizer = pickle.load(open(path_vector, 'rb'))
    db = MyData("english_db.db")

    # Transform and predict input question
    question_x = vectorizer.transform(prepared_question)
    predict_index = model.predict(question_x)
    title_db = db.get_title_by_id(int(predict_index[0]))[0]
    answer = db.get_answers_by_id(int(predict_index[0]))[0]

    similarity = cosine_similarity(prepare_sentence(title_db), prepared_question)
    print("Similarity: ", similarity)
    print("Title_db: ", title_db)
    if similarity < 0.05:
        print("Excuse me, I did not understand that.")
    else:
        print(answer)

    return


print("Hello, this is William. May I help you?")
print("To quit the application select 'q' or 'quit' ")

question = ""
quit_list = ["q", "quit", "break"]

while True:
    print("Please, insert yor question: ")
    question = input().lower()
    if not quit_list.__contains__(question):
        william_response(question)
    else:
        print("Quitting application.\nBye Bye!")
        break
