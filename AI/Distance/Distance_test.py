import os
from DataBase import DB
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from AI.Distance import Distance_Methods as Nlp

# # Phrases to test
# test = Nlp.prepare_sentence("This is a test for my TFG.")
# similar_test = Nlp.prepare_sentence("This follows the test of the TFG")
# not_similar_test = Nlp.prepare_sentence("This question should not be similar.")
#
# # Cosine similarity
# similar_cosine = Nlp.cosine_similarity(test, similar_test)
# not_similar_cosine = Nlp.cosine_similarity(test, not_similar_test)
#
# print("Similar_cosine = ", similar_cosine)
# print("Not_similar_cosine = ", not_similar_cosine)

# In this script we will compare 'Test_Similar_Questions.txt' titles against DB question titles:

# Preparing the data
import nltk
# nltk.download('stopwords')
name_db = "first_db.db"
data = DB.MyData(name_db)
questions_similar = Nlp.read_questions_similar()
questions_DB = data.get_questions_DB()

#  Test:
for question in questions_similar:
    Nlp.select_response(question, questions_DB, "cosine", name_db)

print("------------------------------")
for question in questions_similar:
    Nlp.select_response(question, questions_DB, "jaccard", name_db)

# nlp.Select_Response(questions_similar[5], questions_DB, "jaccard")
