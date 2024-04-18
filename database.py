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
                absense BOOLEAN, 
                censored BOOLEAN, 
                companion_only BOOLEAN, 
                replacements BOOLEAN, 
                replacements_date DATE DEFAULT NULL,
                pray DATE DEFAULT NULL, 
                read_bible DATE DEFAULT NULL, 
                first DATE DEFAULT NULL, 
                revisit DATE DEFAULT NULL, 
                course DATE DEFAULT NULL, 
                speech DATE DEFAULT NULL, 
                read_book DATE DEFAULT NULL, 
                treasures DATE DEFAULT NULL, 
                pearls DATE DEFAULT NULL, 
                book DATE DEFAULT NULL, 
                random DATE DEFAULT NULL, 
                presidency DATE DEFAULT NULL, 
                needs DATE DEFAULT NULL
                )""")
        c.close()

    def create_new(self, values):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        query = "INSERT INTO Witnesses (name, phone, gender, role, absense, censored, companion_only, replacements) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
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
        query = "UPDATE Witnesses SET name = ?, phone = ?, gender = ?, role = ?, absense = ?, censored = ?, companion_only = ?, replacements = ? WHERE id = ?"
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
            "studients": {"read_bible": [], "first": [], "revisit": [], "course": []},
            "studients_plus": {"pray": [], "read_book": []},
            "ministerial": {"treasures": [],"pearls": [], "book": [], "random": []},
            "elder": {"presidency": [], "needs": []}
        }

        cur.execute("SELECT * FROM Witnesses WHERE (role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND censored = 0 ORDER BY read_bible ASC")
        witnesses["studients"]["read_bible"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante' OR role = 'Estudiante +' AND censored = 0 ORDER BY first ASC")
        witnesses["studients"]["first"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante' OR role = 'Estudiante +' AND censored = 0 ORDER BY revisit ASC")
        witnesses["studients"]["revisit"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante' OR role = 'Estudiante +' AND censored = 0 ORDER BY course ASC")
        witnesses["studients"]["course"] = cur.fetchall()

        cur.execute("SELECT * FROM Witnesses WHERE role = 'Estudiante +'")
        witnesses["studients_plus"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Ministerial'")
        witnesses["ministerials"] = cur.fetchall()
        cur.execute("SELECT * FROM Witnesses WHERE role = 'Anciano'")
        witnesses["elders"] = cur.fetchall()

        cur.close()
        return witnesses
