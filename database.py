import sqlite3

class DataBase:
    def __init__(self, table_name):
        self.table_name = table_name
        self.create_database()

    def create_database(self):
        db_connection = sqlite3.connect(self.table_name)
        c = db_connection.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS Witness(name TEXT, phone TEXT, gender TEXT, role TEXT, companion_only BOOLEAN, censored BOOLEAN, replacements BOOLEAN, replacements_date DATE, pray DATE, read_bible DATE, first DATE, revisit DATE, course DATE, speech DATE, read_book DATE, treasures DATE, pearls DATE, book DATE, random DATE, presidency DATE, needs DATE)""")
        c.close()

    def create_new(self):
        db_connection = sqlite3.connect(self.table_name)
        c = db_connection.cursor()
        c.execute("INSERT INTO Studient VALUES ('', '', '', '', '', '', '', '', '', '', '', '', '', '')")
        c.close()