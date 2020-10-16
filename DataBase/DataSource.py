import sqlite3
import os
import rootpath
import csv


class data(object):
    def __init__(self, name):
        root_dir = rootpath.detect()
        # root_dir = os.path.dirname(os.path.abspath(os.curdir))
        # print(root_dir)
        self.path = os.path.join(root_dir, "DataBase", name)
        # print(self.path)
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    # def clear_tables(self):
    #     with self.conn:
    #         self.cursor.execute("DELETE FROM questions")
    #         self.cursor.execute("DELETE FROM answers")
    #     self.cursor.execute("VACUUM")

    def insert_question(self, id_, title, link):
        with self.conn:
            self.cursor.execute("INSERT INTO questions VALUES (:id, :title, :link)",
                                {'id': id_, 'title': title, 'link': link})

    def insert_answer(self, id_, answer):
        with self.conn:
            self.cursor.execute("INSERT INTO answers VALUES (:id, :answer)", {'id': id_, 'answer': answer})

    def get_answers_by_id(self, id_):
        self.cursor.execute("SELECT answer FROM answers WHERE id=:id", {'id': id_})
        return self.cursor.fetchone()

    def get_title_by_id(self, id_):
        self.cursor.execute("SELECT title FROM questions WHERE id=:id", {'id': id_})
        return self.cursor.fetchone()

    def is_question_title_in_DB(self, title):
        self.cursor.execute("SELECT id FROM questions WHERE title=:title", {'title': title})
        if len(self.cursor.fetchall()) > 0:
            return True
        else:
            return False

    def get_last_id(self):
        self.cursor.execute("SELECT COUNT(*) FROM answers")
        return self.cursor.fetchone()[0]

    def get_questions_DB(self):
        questions_db = []
        id_ = 1
        while id_ < self.get_last_id():
            questions_db.append(str(self.get_title_by_id(id_)[0]))
            id_ += 1
        return questions_db

    def get_questions_and_id_dB(self):
        questions_db = []
        id_ = 1
        while id_ < self.get_last_id():
            question = [str(self.get_title_by_id(id_)[0]), id_]
            questions_db.append(question)
            id_ += 1
        return questions_db
