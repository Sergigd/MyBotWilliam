import sqlite3
import os


class data(object):
    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(os.curdir))
        self.path = os.path.join(root_dir, "DataBase", "chatBot.db")
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def insert_request(self, tag, question):
        with self.conn:
            self.cursor.execute("INSERT INTO requests VALUES (:tag, :question)", {'tag': tag, 'question': question})

    def insert_response(self, tag, answer):
        with self.conn:
            self.cursor.execute("INSERT INTO responses VALUES (:tag, :answer)", {'tag': tag, 'answer': answer})

    def get_answers_by_tag(self, tag):
        self.cursor.execute("SELECT answer FROM responses WHERE tag=:tag", {'tag': tag})
        return self.cursor.fetchall()
