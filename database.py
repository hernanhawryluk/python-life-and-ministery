import sqlite3

class DataBase:
    def __init__(self, table_name):
        self.table_name = table_name
        self.create_database()

    def create_database(self):
        db_connection = sqlite3.connect(self.table_name)
        c = db_connection.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS witnesses(name TEXT, phone TEXT, gender TEXT, pray DATE, read DATE)""")
        c.execute('''CREATE TABLE IF NOT EXISTS Studient
                    (name TEXT, phone TEXT, gender TEXT, pray DATE, read DATE, first DATE, revisit DATE, course DATE, speech DATE)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Ministerial
                    (name TEXT, phone TEXT, gender TEXT, pray DATE, read DATE, treasures DATE, pearls DATE, book DATE, random DATE)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Elder
                    (name TEXT, phone TEXT, gender TEXT, pray DATE, read DATE, treasures DATE, pearls DATE, book DATE, random DATE, presidency DATE, needs DATE)''')
        c.close()