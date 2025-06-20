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


    def create_new_participant(self, values):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        query = "INSERT INTO Witnesses (name, phone, gender, role, exclude, custom, companion_only, replacements) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(query, values)
        con.commit()
        cur.close()


    def read_all_participants_names(self):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT name FROM Witnesses")
        rows = cur.fetchall()
        cur.close()
        return rows
    

    def read_participant(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT * FROM Witnesses WHERE name = ?", (name,))
        rows = cur.fetchall()
        cur.close()
        return rows
    

    def modify_participant(self, id, new_data):
        new_data.append(id)
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        query = "UPDATE Witnesses SET name = ?, phone = ?, gender = ?, role = ?, exclude = ?, custom = ?, companion_only = ?, replacements = ? WHERE id = ?"
        cur.execute(query, new_data)
        con.commit()
        cur.close()


    def delete_participant(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("DELETE FROM Witnesses WHERE name = ?", (name,))
        con.commit()
        cur.close()


    def read_data_for_assignations(self, replacements = False):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        witnesses = {
            "studients": {"read_bible": [], "first": [], "revisit": [], "course": [], "explain": [], "speech": [],"companion_male": [], "companion_female": []},
            "studients_plus": {"initial_pray": [], "ending_pray": [], "read_book": []},
            "ministerials": {"treasures": [],"pearls": [], "book": [], "random_1": [], "random_2": [], "masters": []},
            "elders": {"presidency": [], "needs": []}
        }
        queries = [
            {"role": "studients", "assignation": "read_bible", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0", "order": "read_bible ASC, last_assignation ASC"},
            {"role": "studients", "assignation": "first", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0", "order": "first ASC, last_assignation ASC, gender = 'Mujer' DESC"},
            {"role": "studients", "assignation": "revisit", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0", "order": "revisit ASC, last_assignation ASC, gender = 'Mujer' DESC"},
            {"role": "studients", "assignation": "course", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0 AND custom = 0", "order": "course ASC, last_assignation ASC, gender = 'Mujer' DESC"},
            {"role": "studients", "assignation": "explain", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0 AND custom = 0", "order": "explain ASC, last_assignation ASC"},
            {"role": "studients", "assignation": "companion_male", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0", "order": "companion_male ASC, last_assignation ASC"},
            {"role": "studients", "assignation": "companion_female", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Mujer' AND exclude = 0", "order": "companion_female ASC, last_assignation ASC"},
            {"role": "studients", "assignation": "speech", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0", "order": "speech ASC, last_assignation ASC"},
            {"role": "ministerials", "assignation": "masters", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "masters ASC, last_assignation ASC"},
            {"role": "studients_plus", "assignation": "read_book", "where": "(role = 'Estudiante +' OR role = 'Ministerial') AND exclude = 0", "order": "read_book ASC, last_assignation ASC"},
            {"role": "studients_plus", "assignation": "initial_pray", "where": "(role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0", "order": "initial_pray ASC, last_assignation ASC"},
            {"role": "studients_plus", "assignation": "ending_pray", "where": "(role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0", "order": "ending_pray ASC, last_assignation ASC"},
            {"role": "ministerials", "assignation": "treasures", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "treasures ASC, last_assignation ASC"},
            {"role": "ministerials", "assignation": "pearls", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "pearls ASC, last_assignation ASC"},
            {"role": "ministerials", "assignation": "book", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "book ASC, last_assignation ASC"},
            {"role": "ministerials", "assignation": "random_1", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "random_1 ASC, last_assignation ASC"},
            {"role": "ministerials", "assignation": "random_2", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0", "order": "random_2 ASC, last_assignation ASC"},
            {"role": "elders", "assignation": "presidency", "where": "role = 'Anciano' AND exclude = 0 AND custom = 0", "order": "presidency ASC, last_assignation ASC"},
            {"role": "elders", "assignation": "needs", "where": "role = 'Anciano' AND exclude = 0", "order": "needs ASC, last_assignation ASC"},
        ]

        try:
            if replacements == True:
                for query in queries:
                    cur.execute("SELECT * FROM Witnesses WHERE " + query["where"] + " AND replacements = 1 ORDER BY replacements_date ASC, " + query["order"])
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
        for data in data_dict:
            con = sqlite3.connect(self.table_name)
            cur = con.cursor()
            assignment = data[0]
            titular = data[1]
            week = data[2]
            if len(data) == 4:
                companion = data[3]
                cur.execute(f"UPDATE Witnesses SET {assignment} = '{week}', last_assignation = '{week}' WHERE name = '{titular}'")
                cur.execute(f"UPDATE Witnesses SET companion_male = '{week}', companion_female = '{week}', 'last_assignation' = '{week}' WHERE name = '{companion}'")
            else:
                cur.execute(f"UPDATE Witnesses SET {assignment} = '{week}', last_assignation = '{week}' WHERE name = '{titular}'")
            con.commit()
            cur.close()


    def get_phone_number(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute(f"SELECT phone FROM Witnesses WHERE name = '{name}'")
        rows = cur.fetchall()
        cur.close()

        if rows:
            phone_number = rows[0][0]
            return phone_number
        else:
            return None
        

    def clean(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        assignation_list = ["read_bible", "first", "revisit", "course", "explain", "speech", "companion_male", "companion_female", "initial_pray", "ending_pray", "read_book","treasures","pearls", "book", "random_1", "random_2", "masters", "presidency", "needs", "last_assignation", "replacements_date"]

        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        for assignation in assignation_list:
            cur.execute(f"SELECT name FROM Witnesses WHERE {assignation} > {today}")
            person_list = cur.fetchall()
            if person_list != []:
                for person in person_list:
                    name = person[0]
                    cur.execute(f"UPDATE Witnesses SET {assignation} = NULL WHERE name = '{name}'")
        con.commit()
        cur.close()