import sqlite3

class DataBase:
    def __init__(self):
        self.table_name = "witnesses.db"
        
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

    def read_all_data(self):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        witnesses = {
            "studients": {"read_bible": [], "first": [], "revisit": [], "course": [], "explain": [], "speech": [],"companion_male": [], "companion_female": []},
            "studients_plus": {"initial_pray": [], "ending_pray": [], "read_book": []},
            "ministerials": {"treasures": [],"pearls": [], "book": [], "random_1": [], "random_2": [], "masters": []},
            "elders": {"presidency": [], "needs": []}
        }

        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0 ORDER BY last_assignation DESC, read_bible DESC")
        witnesses["studients"]["read_bible"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante' OR role = 'Estudiante +' AND companion_only = 0 AND exclude = 0 ORDER BY gender = 'Mujer' DESC, last_assignation DESC, first DESC")
        witnesses["studients"]["first"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante' OR role = 'Estudiante +' AND companion_only = 0 AND exclude = 0 ORDER BY gender = 'Mujer' DESC, last_assignation DESC, revisit DESC")
        witnesses["studients"]["revisit"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante' OR role = 'Estudiante +' AND companion_only = 0 AND exclude = 0 ORDER BY gender = 'Mujer' DESC, last_assignation DESC, course DESC")
        witnesses["studients"]["course"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante' OR role = 'Estudiante +' AND companion_only = 0 AND exclude = 0 ORDER BY last_assignation DESC, explain DESC")
        witnesses["studients"]["explain"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0 ORDER BY last_assignation DESC, speech DESC")
        witnesses["studients"]["speech"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0 ORDER BY last_assignation DESC, companion_male DESC")
        witnesses["studients"]["companion_male"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Mujer' AND exclude = 0 ORDER BY last_assignation DESC, companion_female DESC")
        witnesses["studients"]["companion_female"] = cur.fetchall()

        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante +' OR role = 'Ministerial') AND exclude = 0 ORDER BY last_assignation DESC, read_book DESC")
        witnesses["studients_plus"]["read_book"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, initial_pray DESC")
        witnesses["studients_plus"]["initial_pray"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, ending_pray DESC")
        witnesses["studients_plus"]["ending_pray"] = cur.fetchall()

        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Ministerial' or role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, treasures DESC")
        witnesses["ministerials"]["treasures"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Ministerial' or role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, pearls DESC")
        witnesses["ministerials"]["pearls"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Ministerial' or role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, book DESC")
        witnesses["ministerials"]["book"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Ministerial' or role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, random_1 DESC")
        witnesses["ministerials"]["random_1"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Ministerial' or role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, random_2 DESC")
        witnesses["ministerials"]["random_2"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Ministerial' or role = 'Anciano') AND exclude = 0 ORDER BY last_assignation DESC, masters DESC")
        witnesses["ministerials"]["masters"] = cur.fetchall()

        cur.execute("SELECT * FROM Witnesses WHERE role = 'Anciano' AND exclude = 0 ORDER BY last_assignation DESC, presidency DESC")
        witnesses["elders"]["presidency"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Anciano' AND exclude = 0 ORDER BY last_assignation DESC, needs DESC")
        witnesses["elders"]["needs"] = cur.fetchall()

        cur.close()
        return witnesses
