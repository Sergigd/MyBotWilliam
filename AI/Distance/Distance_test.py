import os
from DataBase import DataSource
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from AI.Distance import Distance_Methods as nlp


# In this script we will compare 'Test_Similar_Questions.txt' titles against DB question titles:

# Preparing the data
data = DataSource.data()
questions_similar = nlp.read_questions_similar()
questions_DB = data.get_questions_DB()

#  Test:
# Select_Response("hello , , ?", questions_DB)
nlp.Select_Response(questions_similar[5], questions_DB, "jaccard")
