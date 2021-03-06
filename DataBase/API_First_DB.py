import requests as req
import random
import time
from bs4 import BeautifulSoup
from DataBase import DB


class QuestionAndAnswer:
    def __init__(self, title, text_answer, link):
        self.title = title
        self.text_answer = text_answer
        self.link = link


class Sleep:
    def __init__(self):
        try:
            time.sleep(0.2)
        except Exception as e:
            print(e)


# Methods
def get_request_key():
    return req.get("https://stackoverflow.com/oauth/login_success")


def get_url_questions():
    return """https://api.stackexchange.com/2.2/questions?pagesize=99&order=desc&sort=votes&site=stackoverflow"""


def get_number_random(skip):  # skip is a vector which contains all the index of the requests already used
    for _ in range(1, 150):
        number = random.randint(1, 98)
        if not skip.__contains__(number):
            return number
    return -1


def get_single_from_request(request, number):
    json_req = request.json()
    item = json_req["items"]
    return item[number]


def get_text_accepted_answer(single_question):
    try:
        link_question = single_question["link"]
        accepted_answer_id = single_question["accepted_answer_id"]
        if accepted_answer_id is not None:
            text = souping_text_answer(link_question, accepted_answer_id)
            if text is None:
                return -1
            else:
                return text
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def souping_text_answer(link_question, id_answer):
    try:
        source = req.get(get_link_answer(link_question, id_answer)).text
        soup = BeautifulSoup(source, 'lxml')
        answer = soup.find(id="answer-{}".format(id_answer))
        post_text = answer.find(class_="post-text")
        text = """""" + post_text.get_text()
        return text

    except Exception as e:
        print(e)
        return


def get_link_answer(link_question, answer_id):
    return "" + link_question + "#" + str(answer_id)


def text_without_quotes(text):  # Titles with " are written as '&quot;'
    return str(text).replace('&quot;', '\"')


# Main: Get 30 questions and answers to fill DataBase
get_request_key()
url_questions = get_url_questions()

questions_and_answers = []

requests = req.get(url_questions)
randoms = []

# Obtain 30 questions and answers and put them into 'questions_and_answers'
while len(questions_and_answers) < 30:
    number = get_number_random(randoms)
    if number is not -1:
        single = get_single_from_request(requests, number)
        text_answer = get_text_accepted_answer(single)
        if text_answer is not -1:
            title = text_without_quotes(single["title"])
            link = single["link"]

            question_and_answer = QuestionAndAnswer(title, text_answer, link)
            questions_and_answers.append(question_and_answer)
        Sleep()
    else:
        questions_and_answers = []
        print("Not lucky with randoms. Exiting...")

# Fill DB with q&a:
if questions_and_answers is not None:
    data = DB.MyData("first_db.db")
    for question_and_answer in questions_and_answers:
        # Checks:
        if not data.is_question_title_in_db(question_and_answer.title):
            data.insert_question(id_=data.get_last_id() + 1,
                                 title=question_and_answer.title,
                                 link=question_and_answer.link)
            data.insert_answer(id_=data.get_last_id() + 1,
                               answer=question_and_answer.text_answer)
