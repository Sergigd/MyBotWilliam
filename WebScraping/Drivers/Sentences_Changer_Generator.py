"""
In this script we will append text generated in https://web-hobbies.com/en/tools/sentences-changer-generator/ to our
extended_english_DB.db in order to generate better models
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from AI.Distance import Modify_Strings_Methods as Mds
from DataBase import DB
import os
import time


# Path to opera driver
root_dir = os.path.dirname(os.path.abspath(os.curdir))
path_opera = os.path.join(root_dir, "Drivers", "operadriver.exe")

# Database to append generated questions
db = DB.MyData("extended_english_DB.db")

throw_exception = []
count = 0
try:  # Extract url process
    while db.get_id_of_first_extended_question_null() > 0:
        # Select question to search in the webpage
        question_id = db.get_id_of_first_extended_question_null()
        question_title = db.get_title_by_id(question_id)[0]

        # Exception
        if throw_exception == question_id:
            raise TypeError("Repeated id")
        if count > 0:
            raise KeyError("Not scraped")

        print(question_title)

        # Get the url
        url = Mds.url_changer_text(question_title)
        print(url)
        count += 1

        try:  # Scraping process
            driver = webdriver.Opera(executable_path=path_opera)
            driver.get(url)
            time.sleep(2)
            myElem = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'rewordtext')))
            print("Myelem: ", myElem.get_attribute("value"))
            # WebDriverWait.until(driver.find_element_by_id("rewordtext"))
            # driver.implicitly_wait(10)
            reword = driver.find_element_by_id("rewordtext")
            text = reword.get_attribute("value")

            print(text)
            if text is not "":
                # Update db
                db.update_extended_question(question_id, text)
                throw_exception = question_id
                count = 0
            else:
                raise ValueError("text = ", text)

        except Exception as e2:
            print("Exception in scraping process: ", e2)
        except ValueError as v:
            print("Exception in scraping process: (value error) ", v)
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            driver.close()

            # Time
            time.sleep(1)

except TypeError as io:
    print("Exception in the extract url process, repeated id: ", io)
except TimeoutError as time_error:
    print("TimeoutError: ", time_error)