"""
In this script we will append text generated in https://web-hobbies.com/en/tools/sentences-changer-generator/ to our
extended_english_DB.db in order to generate better models
"""
from DataBase import DataSource
import time
from bs4 import BeautifulSoup
import requests
from AI.Distance import Modify_Strings_Methods as Mds


# db = DataSource.data("extended_english_DB.db")

url = Mds.url_changer_text("This is a test to get different text")
source = requests.get(url, headers={'user-agent': 'my-app/0.0.1'}).text

try:
    soup = BeautifulSoup(source, "lxml")
    owner = soup.find("div", class_="theOwner")
    lastBars = owner.findAll("div", class_="lastBar")

    for textarea in lastBars[0].findAll('textarea'):
        print(textarea)
        print("-----------------------------")

    # print(soup)
    # print()
    # print(owner)
    # print("--------------------------------------")
    # print(textArea)
    # print(soup.text)

except Exception as e:
    print("Exception: ", e)

print(url)
