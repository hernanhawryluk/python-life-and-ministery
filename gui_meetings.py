import customtkinter as ctk
from database import DataBase
from utils_weeks import calculate_weeks

class MeetingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.generated_months = 0
        self.weeks = calculate_weeks(self.generated_months)
        print(self.weeks)
        self.db = DataBase()
        self.assignations = [
            {"key": "precidency", "text": "Presidencia", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "initial_pray","text": "Oración inicial", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]}, 
            {"key": "treasures", "text": "Tesoros de la Biblia", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "pearls", "text": "Busquemos Perlas Escondidas", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "read_bible","text": "Lectura de la Biblia", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "school_1", "text": "Escuela Asignación 1", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "school_2", "text": "Escuela Asignación 2", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "school_3", "text": "Escuela Asignación 3", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "school_4", "text": "Escuela Asignación 4", "state": "normal", "school": True, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "random_1", "text": "Asignación 1", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "random_2", "text": "Asignación 2", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "book", "text": "Estudio Biblico de Congregación", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "read_book", "text": "Lectura en Estudio Biblico", "state": "normal", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            {"key": "ending_pray", "text": "Oración final", "state": "disabled", "school": False, "values": ["Opción 1", "Opción 2", "Opción 3"]},
            ]
        
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text="", font=("Arial", 16), width=0, state=value["state"], text_color_disabled="#FFFFFF")
                self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], width=250)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=value["values"], width=270)
                self.widgets["option2_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=value["values"], width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)
                self.widgets["option2_" + self.assignations[i]["key"]].grid(row=i, column=3, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=value["values"], width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)

        self.buttonGenerate = ctk.CTkButton(master=master, text="Saltar Semana", width=300, height=40, command=self.skip_week)
        self.labelWeek = ctk.CTkLabel(master=master, text=self.weeks[0], width=270, height=40)
        print(self.weeks[0])
        self.buttonSave = ctk.CTkButton(master=master, text="Guardar Semana", width=270, height=40, command=self.save_week)

        self.buttonGenerate.grid(row=14, column=0, padx=10, pady=(20, 10),columnspan=2)
        self.labelWeek.grid(row=14, column=2, padx=10, pady=(20, 10))
        self.buttonSave.grid(row=14, column=3, padx=10, pady=(20, 10), columnspan=1)

        self.generate_week()

    def generate_week(self):
        self.all_witnesses = self.db.read_all_data()
        self.studients = self.all_witnesses["studients"]
        self.studients_plus = self.all_witnesses["studients_plus"]
        self.ministers = self.all_witnesses["ministerials"]
        self.ancients = self.all_witnesses["elders"]
        print(self.studients)



    def skip_week(self):
        self.weeks.pop(0)
        if self.weeks == []:
            self.generated_months += 1
            self.weeks = calculate_weeks(self.generated_months)
        self.labelWeek.configure(text=self.weeks[0])
        pass

    def save_week(self):
        pass