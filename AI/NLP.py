import os
import nltk
from DataBase import DataSource
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


# In this script we will compare 'Test_Similar_Questions.txt' titles against DB question titles:
class Question:
    def __init__(self, text, id_):
        self.text = text
        self.id = id_


def prepare_sentence(sentence):
    words_token = word_tokenize(sentence)

    stemmer = SnowballStemmer("english")

    words_stem = []
    for word in words_token:
        words_stem.append(stemmer.stem(word))

    stop_words = set(stopwords.words('english'))
    words_stopped = [sp for sp in words_stem if sp not in stop_words]
    return words_stopped


def Select_Response(title, questions):
    title_prepared = prepare_sentence(title)

    # cosine similarity:
    cosine_indexes = []
    cosine_indexes_2 = []
    for question in questions:
        vector_title = []
        vector_question = []

        question_prepared = prepare_sentence(question)
        r_vector = set().union(*[tuple(title_prepared), tuple(question_prepared)])

        for w in r_vector:
            if w in title_prepared:
                vector_title.append(1)  # create a vector
            else:
                vector_title.append(0)
            if w in question_prepared:
                vector_question.append(1)
            else:
                vector_question.append(0)

        c = 0
        # cosine formula: Similarity = (A.B) / (||A||.||B||) where A and B are vectors.
        for i in range(len(r_vector)):
            c += vector_title[i] * vector_question[i]
        cosine = c / float((sum(vector_title) * sum(vector_question)) ** 0.5)
        cosine_indexes.append(cosine)

    print(cosine_indexes)
    maximum = max(cosine_indexes)
    print("Max similarity: ", maximum)

    index = cosine_indexes.index(maximum)
    id_ = index + 1

    print(title)
    print(questions_DB[index])

    print(cosine_indexes_2)

questions_similar = []
questions_DB = []
data = DataSource.data()

# Reading the data
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path = os.path.join(root_dir, "AI", "Test_Similar_Questions.txt")
with open(path) as f:
    for num, line in enumerate(f, 1):
        line = str(line).lower()
        question = Question(line, num)
        questions_similar.append(question)

id_ = 1
while id_ < data.get_last_id():
    questions_DB.append(str(data.get_title_by_id(id_)[0]))
    id_ += 1

#  Test:
Select_Response(questions_similar[10].text, questions_DB)
