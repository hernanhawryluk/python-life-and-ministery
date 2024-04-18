import customtkinter as ctk

class MeetingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
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
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=value["values"], width=200)
                self.widgets["option2_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=value["values"], width=200)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)
                self.widgets["option2_" + self.assignations[i]["key"]].grid(row=i, column=4, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=value["values"], width=200)
                
                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)

        self.buttonNew = ctk.CTkButton(master=master, text="Nueva Semana", width=100, height=40)
        self.buttonGenerate = ctk.CTkButton(master=master, text="Generar Semana", width=100, height=40)
        self.buttonSave = ctk.CTkButton(master=master, text="Guardar Semana", width=100, height=40)
        self.buttonNew.grid(row=14, column=0, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)
        self.buttonGenerate.grid(row=14, column=2, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)
        self.buttonSave.grid(row=14, column=4, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)