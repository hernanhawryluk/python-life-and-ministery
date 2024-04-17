import sqlite3
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Reuniones Vida y Ministerio Teocrático")
        self.geometry("930x810")

        self.tab_view = TabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10)

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Reuniones")
        self.add("Remplazos")
        self.add("Participantes")

        self.meetings_frame = TreasuresFrame(master=self.tab("Reuniones"))


class TreasuresFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.assignations = [
            {"text": "Presidencia", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Oración inicial", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]}, 
            {"text": "Tesoros de la Biblia", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Busquemos Perlas Escondidas", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Lectura de la Biblia", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Escuela Asignación 1", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Escuela Asignación 2", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Escuela Asignación 3", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Escuela Asignación 3", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Asignación 1", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Asignación 2", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Estudio Biblico de Congregación", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Lectura en Estudio Biblico", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"text": "Oración final", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            ]

        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.checkbox = ctk.CTkCheckBox(master=master, text="", font=("Arial", 18), width=0, state=value["state"], text_color_disabled="#FFFFFF")
                self.checkbox.select()
                self.option = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], width=250)
                self.option1 = ctk.CTkOptionMenu(master=master, values=value["values"], width=200)
                self.option2 = ctk.CTkOptionMenu(master=master, values=value["values"], width=200)
                self.button = ctk.CTkButton(master=master, text="Reroll", width=30)
                self.button1 = ctk.CTkButton(master=master, text="Reroll", width=30)

                self.checkbox.grid(row=i, column=0, padx=10, pady=10)
                self.option.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.option1.grid(row=i, column=2, padx=10, pady=10)
                self.button.grid(row=i, column=3, padx=10, pady=10)
                self.option2.grid(row=i, column=4, padx=10, pady=10)
                self.button1.grid(row=i , column=5, padx=10, pady=10)

            else:
                self.checkbox = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 18), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                self.checkbox.select()
                self.option = ctk.CTkOptionMenu(master=master, values=value["values"], width=200)
                self.button = ctk.CTkButton(master=master, text="Reroll", width=30)
                self.checkbox.grid(row=i, column=0, columnspan=2, padx=10, pady=10)
                self.option.grid(row=i, column=2, padx=10, pady=10)
                self.button.grid(row=i, column=3, padx=10, pady=10)

        self.buttonNew = ctk.CTkButton(master=master, text="Nueva Semana", width=100, height=40)
        self.buttonGenerate = ctk.CTkButton(master=master, text="Generar Semana", width=100, height=40)
        self.buttonSave = ctk.CTkButton(master=master, text="Guardar Semana", width=100, height=40)
        self.buttonNew.grid(row=14, column=0, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)
        self.buttonGenerate.grid(row=14, column=2, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)
        self.buttonSave.grid(row=14, column=4, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)

class DataBase:
    def __init__(self, table_name):
        self.table_name = table_name
        self.create_database()

    def create_database(self):
        db_connection = sqlite3.connect(self.table_name)
        c = db_connection.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS witnesses(name TEXT, gender TEXT, pray DATE, read DATE)""")
        c.execute('''CREATE TABLE IF NOT EXISTS Studient
                    (name TEXT, gender TEXT, pray DATE, read DATE, first DATE, revisit DATE, course DATE, speech DATE)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Ministerial
                    (name TEXT, gender TEXT, pray DATE, read DATE, treasures DATE, pearls DATE, book DATE, random DATE)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Elder
                    (name TEXT, gender TEXT, pray DATE, read DATE, treasures DATE, pearls DATE, book DATE, random DATE, presidency DATE, needs DATE)''')
        c.close()
            
if __name__ == "__main__":
    db = DataBase("witnesses.db")
    app = App()
    app.mainloop()
