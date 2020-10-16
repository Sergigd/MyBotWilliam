from langdetect import detect
from AI.Distance import Distance_Methods as DM
#
# print(detect("Esto es una prueba"))
# print(detect("Also is this"))
# print(detect("Per descomptat, això també ho és"))

# for question in DM.read_questions_similar():
#     print(question)
#     print(detect(question))
#     print("-----")


def language_detect(text):
    return detect(text)
