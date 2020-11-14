import sqlite3
import os
import rootpath
import csv


class MyData(object):
    def __init__(self, name):
        root_dir = rootpath.detect()
        self.path = os.path.join(root_dir, "DataBase", name)
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

    def get_link_by_id(self, id_):
        self.cursor.execute("SELECT link FROM questions WHERE id=:id", {'id': id_})
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

    def get_all_titles(self):
        self.conn.row_factory = lambda cursor, row: row[0]
        c = self.conn.cursor()
        c.execute("SELECT title FROM questions")
        return c.fetchall()

    def get_all_generated_titles(self):
        self.conn.row_factory = lambda cursor, row: row[0]
        c = self.conn.cursor()
        c.execute("SELECT generated_title FROM questions")
        return c.fetchall()



    def get_all_ids(self):
        self.conn.row_factory = lambda cursor, row: row[0]
        c = self.conn.cursor()
        c.execute("SELECT id FROM questions")
        return c.fetchall()

    def get_id_by_title(self, title):
        self.cursor.execute("SELECT id FROM questions WHERE title=:title", {'title': title})
        return self.cursor.fetchone()

    def get_id_of_first_extended_question_null(self):
        self.cursor.execute("SELECT id FROM questions WHERE generated_title is NULL")
        return self.cursor.fetchone()[0]

    def update_extended_question(self, id_, text):
        with self.conn:
            # self.cursor.execute("UPDATE questions SET generated_title=NULL WHERE generated_title=''")
            self.cursor.execute("UPDATE questions SET generated_title=:text WHERE id=:id_", {'text': text, 'id_': id_})