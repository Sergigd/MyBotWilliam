from DataBase import DB
from AI.Distance import Distance_Methods as Nlp
import time

time_start = time.time()

name_db = "first_db.db"
type_similarity = "jaccard"  # "cosine"
data = DB.MyData(name_db)

questions_similar = Nlp.read_questions_similar_with_check()
questions_DB = data.get_questions_db()

#  Test:
good = 0
attempts = 0
for question in questions_similar:
    title = Nlp.select_response(question[0], questions_DB, "jaccard")
    attempts += 1
    if title == question[1]:
        good += 1

time_finish = time.time()
total_time = time_finish - time_start
print("Time = ", total_time, " Good = ", good, " accuracy = ", good/attempts)
