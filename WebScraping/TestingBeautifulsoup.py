from bs4 import BeautifulSoup
import requests

# question = input("What do you want?\n")
# Con una funcion convertir la pregunta en codigo de la busqueda( mezcla de unicode y letras)

question = "AttributeError: 'NoneType' object has no attribute 'clear'"


def textToSearch(sentence="Testing"):
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
soup = BeautifulSoup(source, "lxml")
print(soup.prettify())

# div = soup.find("div", class_="ps-relative")
# find_input = div.find("input")
# value = find_input.find("value")
# value.string = question
# print(value)
#

