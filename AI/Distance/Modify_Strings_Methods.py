
def text_to_search(sentence="Testing"):  # =Testing para asegurar que sea un string y me deje hacer el replace
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


def url_changer_text(sentence="Testing"):
    sentence = sentence.replace("%", " percent", -1)
    sentence = sentence.replace(" ", "%20", -1)
    sentence = sentence.replace(".", "", -1)
    sentence = sentence.replace("#", "", -1)

    return "https://web-hobbies.com/en/tools/sentences-changer-generator/?text=" + sentence + \
               "&indice=0&isCapital=false&PosNeg=1"

def modify_title(sentence="Testing"):
    sentence = sentence.replace('&quot;', '\"')
    sentence = sentence.replace("&#39;", "'", -1)
    # sentence = sentence.replace(" ", "+", -1)
    return sentence
