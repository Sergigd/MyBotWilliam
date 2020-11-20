from DataBase import DB
from DataBase import API_StackExchange as Api
from os import remove
from AI.Distance import Modify_Strings_Methods as Modify

# Main: fill 'english_DB' with questions of Stack's API. Looping over weeks and obtaining responded questions.
data = DB.MyData("english_db.db")
while data.get_last_id() < 10000:
    file_dates = "Stack_dates_en.txt"
    with open("Stack_dates_en.txt", 'r') as file:
        line = file.read().split(",")
        year = int(line[0])
        month = int(line[1])
        day = int(line[2])

    month_list = [4, 6, 9, 11]
    if month_list.__contains__(month):
        if day == 30:
            n_month = month + 1
            n_day = 1
            n_year = year
        else:
            n_month = month
            n_day = day + 1
            n_year = year

    elif month == 2:
        if day == 27:
            n_month = month + 1
            n_day = 1
            n_year = year
        else:
            n_month = month
            n_day = day + 1
            n_year = year
    else:
        if day == 31:
            n_day = 1
            if month == 12:
                n_year = year + 1
                n_month = 1
            else:
                n_year = year
                n_month = month + 1
        else:
            n_month = month
            n_day = day + 1
            n_year = year

    print("¿?: year = ", n_year, " month = ", n_month, " day = ", n_day)

    url_questions = "" + Api.get_url_questions_dates((year, month, day, 0, 0, 0, 0, 0, 0),
                                                     (n_year, n_month, n_day, 0, 0, 0, 0, 0, 0))
    requests = Api.get_requests(url_questions)

    if requests.text == "To Many Requests":
        url_questions = "" + Api.get_url_questions_dates((year, month, day, 12, 0, 0, 0, 0, 0),
                                                         (n_year, n_month, n_day, 0, 0, 0, 0, 0, 0))
        requests = Api.get_requests(url_questions)

    questions_and_answers = []
    for num, single in enumerate(requests.json()["items"]):
        text_answer = Api.get_text_accepted_answer(single)
        if text_answer is not -1:
            title = Modify.modify_title(single["title"])
            link = single["link"]
            question_and_answer = Api.QuestionAndAnswer(title, text_answer, link)
            questions_and_answers.append(question_and_answer)

    # Fill DB with q&a:
    if questions_and_answers is not None:
        for question_and_answer in questions_and_answers:
            data = DB.MyData("english_db.db")
            if not data.is_question_title_in_DB(question_and_answer.title):
                data.insert_question(id_=data.get_last_id() + 1,
                                     title=question_and_answer.title,
                                     link=question_and_answer.link)
                data.insert_answer(id_=data.get_last_id() + 1,
                                   answer=question_and_answer.text_answer)

    print("Added to DB: year = ", n_year, " month = ", n_month, " day = ", n_day)
    remove(file_dates)
    with open(file_dates, 'w') as file:
        file.write("" + str(n_year) + "," + str(n_month) + "," + str(n_day))

    print("Hay en la BD: ", data.get_last_id())
