from DataBase import DB
from AI.Distance import Distance_Methods as Nlp
import time

name_db = "first_db.db"
data = DB.MyData(name_db)
questions_similar = Nlp.read_questions_similar()
questions_DB = data.get_questions_DB()

#  Test:
time_start = time.time()
for question in questions_similar:
    Nlp.select_response(question, questions_DB, "jaccard")

time_finish = time.time()
total_time = time_finish - time_start
print("Time = ", total_time)
print("------------------------------")
# for question in questions_similar:
#     Nlp.select_response(question, questions_DB, "jaccard", name_db)

# nlp.Select_Response(questions_similar[5], questions_DB, "jaccard")
