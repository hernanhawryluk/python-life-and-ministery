import os
import sqlite3
import datetime

class DataBase:
    def __init__(self):
        self.table_name = os.path.join("data", "witnesses.db")
        
    def create_database(self):
        db_connection = sqlite3.connect(self.table_name)
        c = db_connection.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS Witnesses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, 
                phone TEXT, 
                gender TEXT, 
                role TEXT, 
                exclude BOOLEAN, 
                custom BOOLEAN, 
                companion_only BOOLEAN, 
                replacements BOOLEAN, 
                replacements_date DATE DEFAULT NULL,
                initial_pray DATE DEFAULT NULL, 
                ending_pray DATE DEFAULT NULL,
                read_bible DATE DEFAULT NULL, 
                first DATE DEFAULT NULL, 
                revisit DATE DEFAULT NULL, 
                course DATE DEFAULT NULL, 
                explain DATE DEFAULT NULL,
                speech DATE DEFAULT NULL, 
                companion_male DATE DEFAULT NULL, 
                companion_female DATE DEFAULT NULL,
                read_book DATE DEFAULT NULL, 
                treasures DATE DEFAULT NULL, 
                pearls DATE DEFAULT NULL, 
                book DATE DEFAULT NULL, 
                random_1 DATE DEFAULT NULL, 
                random_2 DATE DEFAULT NULL,
                masters DATE DEFAULT NULL,
                presidency DATE DEFAULT NULL, 
                needs DATE DEFAULT NULL,
                last_assignation DATE DEFAULT NULL
                )""")
        c.close()

    def create_new(self, values):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        query = "INSERT INTO Witnesses (name, phone, gender, role, exclude, custom, companion_only, replacements) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(query, values)
        con.commit()
        cur.close()

    def read_all_names(self):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT name FROM Witnesses")
        rows = cur.fetchall()
        cur.close()
        return rows
    
    def read_one(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT * FROM Witnesses WHERE name = ?", (name,))
        rows = cur.fetchall()
        cur.close()
        return rows
    
    def modify_one(self, id, new_data):
        new_data.append(id)
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        query = "UPDATE Witnesses SET name = ?, phone = ?, gender = ?, role = ?, exclude = ?, custom = ?, companion_only = ?, replacements = ? WHERE id = ?"
        cur.execute(query, new_data)
        con.commit()
        cur.close()

    def delete_one(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("DELETE FROM Witnesses WHERE name = ?", (name,))
        con.commit()
        cur.close()

    def read_all_data(self, replacements = False):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        witnesses = {
            "studients": {"read_bible": [], "first": [], "revisit": [], "course": [], "explain": [], "speech": [],"companion_male": [], "companion_female": []},
            "studients_plus": {"initial_pray": [], "ending_pray": [], "read_book": []},
            "ministerials": {"treasures": [],"pearls": [], "book": [], "random_1": [], "random_2": [], "masters": []},
            "elders": {"presidency": [], "needs": []}
        }
        queries = [
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0", "order": "last_assignation DESC, read_bible ASC", "role": "studients", "assignation": "read_bible"},
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0", "order": "gender = 'Mujer' DESC, last_assignation DESC, first ASC", "role": "studients", "assignation": "first"},
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0", "order": "gender = 'Mujer' DESC, last_assignation DESC, revisit ASC", "role": "studients", "assignation": "revisit"},
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0 AND custom = 0", "order": "gender = 'Mujer' DESC, last_assignation DESC, course ASC", "role": "studients", "assignation": "course"},
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0 AND custom = 0", "order": "last_assignation DESC, explain ASC", "role": "studients", "assignation": "explain"},
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0", "order": "last_assignation ASC, companion_male ASC", "role": "studients", "assignation": "companion_male"},
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Mujer' AND exclude = 0", "order": "last_assignation ASC, companion_female ASC", "role": "studients", "assignation": "companion_female"},
            {"where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0", "order": "last_assignation DESC, speech ASC", "role": "studients", "assignation": "speech"},
            {"where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, masters ASC", "role": "ministerials", "assignation": "masters"},
            {"where": "(role = 'Estudiante +' OR role = 'Ministerial') AND exclude = 0", "order": "last_assignation DESC, read_book ASC", "role": "studients_plus", "assignation": "read_book"},
            {"where": "(role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, initial_pray ASC", "role": "studients_plus", "assignation": "initial_pray"},
            {"where": "(role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, ending_pray ASC", "role": "studients_plus", "assignation": "ending_pray"},
            {"where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, treasures ASC", "role": "ministerials", "assignation": "treasures"},
            {"where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, pearls ASC", "role": "ministerials", "assignation": "pearls"},
            {"where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, book ASC", "role": "ministerials", "assignation": "book"},
            {"where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, random_1 ASC", "role": "ministerials", "assignation": "random_1"},
            {"where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "last_assignation DESC, random_2 ASC", "role": "ministerials", "assignation": "random_2"},
            {"where": "role = 'Anciano' AND exclude = 0 AND custom = 0", "order": "last_assignation DESC, presidency ASC", "role": "elders", "assignation": "presidency"},
            {"where": "role = 'Anciano' AND exclude = 0", "order": "last_assignation DESC, needs ASC", "role": "elders", "assignation": "needs"},
        ]

        try:
            if replacements == True:
                for query in queries:
                    cur.execute("SELECT * FROM Witnesses WHERE " + query["where"] + " AND replacements = 1 ORDER BY " + query["order"])
                    witnesses[query["role"]][query["assignation"]] = cur.fetchall()
            else:
                for query in queries:
                    cur.execute("SELECT * FROM Witnesses WHERE " + query["where"] + " ORDER BY " + query["order"])
                    witnesses[query["role"]][query["assignation"]] = cur.fetchall()
        except Exception as e:
            print(e)

        cur.close()
        return witnesses
    
    def write_data(self, data_dict):
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        for data in data_dict:
            print(data)
            con = sqlite3.connect(self.table_name)
            cur = con.cursor()
            if len(data) == 3:
                cur.execute(f"UPDATE Witnesses SET '{data[0]}' = '{today}' WHERE name = '{data[1]}'")
                cur.execute(f"UPDATE Witnesses SET companion_male = '{today}', companion_female = '{today}' WHERE name = '{data[2]}'")
            else:
                cur.execute(f"UPDATE Witnesses SET '{data[0]}' = '{today}' WHERE name = '{data[1]}'")
            con.commit()
            cur.close()

