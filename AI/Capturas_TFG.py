from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from AI.Distance import Distance_Methods as msd


def prepare_sentence(sentence):
    # Tokenize
    words_token = word_tokenize(sentence)

    print(type(words_token))

    # Stemming
    stemmer = SnowballStemmer("english")
    words_stem = []
    for word in words_token:
        words_stem.append(stemmer.stem(word))

    # Stop words
    stop_words = set(stopwords.words('english'))
    words_stopped = [sp for sp in words_stem if sp not in stop_words]

    return words_stopped


test = prepare_sentence("This is a test for my TFG: Testing")
t = msd.cosine_similarity(test, test)
print(type(t))