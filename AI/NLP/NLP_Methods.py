import os
from DataBase import DataSource
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


def read_questions_similar():
    # Reading the data
    questions_similar = []
    root_dir = os.path.dirname(os.path.abspath(os.curdir))
    path = os.path.join(root_dir, "AI", "NLP", "Test_Similar_Questions.txt")
    with open(path) as f:
        for line in f:
            line = str(line).lower()
            questions_similar.append(line)
    return questions_similar


def get_answer_by_id(_id):
    data = DataSource.data()
    return str(data.get_answers_by_id(_id)[0])


def prepare_sentence(sentence):
    words_token = word_tokenize(sentence)

    stemmer = SnowballStemmer("english")

    words_stem = []
    for word in words_token:
        words_stem.append(stemmer.stem(word))

    stop_words = set(stopwords.words('english'))
    stop_words.add("?")
    stop_words.add(",")
    stop_words.add("(")
    stop_words.add(")")
    stop_words.add("{")
    stop_words.add("}")
    words_stopped = [sp for sp in words_stem if sp not in stop_words]
    return words_stopped


def cosine_similarity(title_prep, question_prep):
    vector_title = []
    vector_question = []
    r_vector = set().union(*[tuple(title_prep), tuple(question_prep)])
    for w in r_vector:
        if w in title_prep:
            vector_title.append(1)  # create a vector
        else:
            vector_title.append(0)
        if w in question_prep:
            vector_question.append(1)
        else:
            vector_question.append(0)

    c = 0
    # cosine formula: Similarity = (A.B) / (||A||.||B||) where A and B are vectors.
    for i in range(len(r_vector)):
        c += vector_title[i] * vector_question[i]
    cosine = c / float((sum(vector_title) * sum(vector_question)) ** 0.5)
    return cosine


def Select_Response(title, questions):
    title_prepared = prepare_sentence(title)

    # cosine similarity:
    cosine_indexes = []
    for question in questions:
        question_prepared = prepare_sentence(question)
        cosine = cosine_similarity(title_prepared, question_prepared)
        cosine_indexes.append(cosine)

    print(cosine_indexes)
    maximum = max(cosine_indexes)
    print("Max similarity: ", maximum)

    if maximum < 0.3:
        print(title)
        print("No coincidence.")
    else:
        index = cosine_indexes.index(maximum)

        print(title)
        print(questions[index])
        print(get_answer_by_id(_id=index+1))


def extract_comas(sentence):
    stop_words = [","]
    words = [str(word) for word in sentence if word not in stop_words]
    sentence_extracted = ""
    sentence_extracted = sentence_extracted.join(words)
    return sentence_extracted
