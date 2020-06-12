import sqlite3

DB_NAME = "chatBot.db"

try:
    conn = sqlite3.connect(DB_NAME)

    c = conn.cursor()

    # c.execute("""CREATE TABLE requests (
    #             tag text,
    #             question text
    #             )""")
    # c.execute("""CREATE TABLE responses (
    #             tag text,
    #             answer text
    #             )""")
    # conn.commit()

    conn.close()
except sqlite3.Error as e:
    print("TEST: ", str(e))
