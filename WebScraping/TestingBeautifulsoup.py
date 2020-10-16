from bs4 import BeautifulSoup
import requests

# question = input("What do you want?\n")
# Con una función convertir la pregunta en codigo de la busqueda( mezcla de unicode y letras)

question = "AttributeError: 'NoneType' object has no attribute 'clear'"
q2 = "IndexError: list index out of range"


def textToSearch(sentence="Testing"):  # =Testing para asegurar que sea un string y me deje hacer el replace
    sentence = sentence.replace("%", "%25", -1)

    sentence = sentence.replace("'", "%27", -1)
    sentence = sentence.replace("?", "%3F", -1)
    sentence = sentence.replace("!", "%21", -1)
    sentence = sentence.replace("$", "%24", -1)
    sentence = sentence.replace("&", "%26", -1)
    sentence = sentence.replace("/", "%2F", -1)
    sentence = sentence.replace("\"", "%5C", -1)
    sentence = sentence.replace("(", "%28", -1)
    sentence = sentence.replace(")", "%29", -1)
    sentence = sentence.replace("=", "%3D", -1)
    sentence = sentence.replace("+", "%2B", -1)
    sentence = sentence.replace(",", "%2C", -1)
    sentence = sentence.replace(";", "%3B", -1)
    sentence = sentence.replace(":", "%3A", -1)
    sentence = sentence.replace("{", "%7B", -1)
    sentence = sentence.replace("}", "%7D", -1)

    sentence = sentence.replace(" ", "+", -1)
    return sentence


question = textToSearch(question)

source = requests.get("https://stackoverflow.com/search?q={value}".format(value=question)).text
source = requests.get("https://stackoverflow.com/questions/12051/calling-the-base-constructor-in-c-sharp").text
soup = BeautifulSoup(source, "lxml")
answer = soup.find("div", class_="answer accepted-answer")
t = answer.find("div", class_="s-prose js-post-body")
print(t.get_text())

# div = soup.find("div", class_="ps-relative")
# find_input = div.find("input")
# value = find_input.find("value")
# value.string = question
# print(value)
#
