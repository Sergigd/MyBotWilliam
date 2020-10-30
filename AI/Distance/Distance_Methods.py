import os
from DataBase import DataSource
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.metrics import jaccard_score


def read_questions_similar():
    # Reading the data
    questions_similar = []
    root_dir = os.path.dirname(os.path.abspath(os.curdir))
    path = os.path.join(root_dir, "AI", "Distance", "Test_Similar_Questions.txt")
    # path = os.path.join(root_dir, "Distance", "Test_Similar_Questions.txt")
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

    # create a vector with 1 and 0
    for w in r_vector:
        if w in title_prep:
            vector_title.append(1)
        else:
            vector_title.append(0)
        if w in question_prep:
            vector_question.append(1)
        else:
            vector_question.append(0)

    # cosine formula: Similarity = (A.B) / (||A||.||B||) where A and B are vectors.
    c = 0
    for i in range(len(r_vector)):
        c += vector_title[i] * vector_question[i]
    cosine = c / float((sum(vector_title) * sum(vector_question)) ** 0.5)
    return cosine

#
# def jaccard2_similarity(title_prep, question_prep):
#     print(title_prep)
#     print(question_prep)
#
#     score = jaccard_score(title_prep, question_prep, average="weighted")
#     print(score)
#     return score


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def select_response(title, questions, method="cosine"):
    title_prepared = prepare_sentence(title)

    similarity_indexes = []
    if method == "cosine":
        # cosine similarity:
        for question in questions:
            question_prepared = prepare_sentence(question)
            cosine = cosine_similarity(title_prepared, question_prepared)
            similarity_indexes.append(cosine)
    elif method == "jaccard":
        for question in questions:
            question_prepared = prepare_sentence(question)
            jaccard = jaccard_similarity(title_prepared, question_prepared)
            similarity_indexes.append(jaccard)
    else:
        print("There is no method called: ", method)
        return -1

    print(similarity_indexes)
    maximum = max(similarity_indexes)
    print("Max similarity: ", maximum)

    if maximum < 0.3:
        print(title)
        print("No coincidence.")
    else:
        index = similarity_indexes.index(maximum)

        print(title)
        print(questions[index])
        print(get_answer_by_id(_id=index + 1))


def extract_comas(sentence):
    stop_words = [","]
    words = [str(word) for word in sentence if word not in stop_words]
    sentence_extracted = ""
    sentence_extracted = sentence_extracted.join(words)
    return sentence_extracted
