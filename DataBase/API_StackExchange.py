import requests as req
from bs4 import BeautifulSoup
import time


def get_client_id():
    return """18769"""


def get_app_key():
    return "FyOCVccuKZAE)53OeZ874Q(("


def get_access_token():
    # url = "https://stackexchange.com/oauth/dialog?client_id={" \
    #       "0}&scope=&redirect_uri=https://stackexchange.com/oauth/login_success/".format(get_client_id())
    # print(url)
    return "aZrdUopB9QJe04F30Pmt1w))"


def get_url_questions():
    url = "https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow&key=" \
          + get_app_key() + "&access_token=" + get_access_token() + "&filter=withbody"
    return url


def get_url_questions_dates(from_date, to_date):
    from_ = str(time.mktime(from_date).__trunc__())
    to_ = str(time.mktime(to_date).__trunc__())
    url = "https://api.stackexchange.com/2.2/questions?fromdate=" + from_ + "&todate=" + to_ + \
          "&pagesize=99&order=desc&sort=votes&site=stackoverflow&key=" + get_app_key() + "&access_token=" + \
          get_access_token() + "&filter=withbody"
    return url


def get_requests(url):
    return req.get(url)


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
        # print("Exception: ", e)
        return -1


def souping_text_answer(link_question, id_answer):
    try:
        source = req.get(get_link_answer(link_question, id_answer)).text
        soup = BeautifulSoup(source, 'lxml')
        answer = soup.find("div", class_="answer accepted-answer")
        post_text = answer.find("div", class_="s-prose js-post-body")
        # answer = soup.find(id="answer-{}".format(id_answer))
        # post_text = answer.find(class_="post-layout")
        text = "" + post_text.get_text()
        # print(text)
        return text

    except Exception as e:
        # print("Exception: ", e)
        return


def get_link_answer(link_question, answer_id):
    return "" + link_question + "#" + str(answer_id)



class QuestionAndAnswer:
    def __init__(self, title, text_answer, link):
        self.title = title
        self.text_answer = text_answer
        self.link = link
