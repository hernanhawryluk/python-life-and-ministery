import customtkinter as ctk
from database import DataBase
from utils_switchers import school_switcher

class ReplacementsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.db = DataBase()
        self.witnesses_excluded = []

        self.assignations = [
            {"key": "presidency", "text": "Presidencia", "state": "normal", "school": False, "role": "elders"},
            {"key": "initial_pray","text": "Oración inicial", "state": "normal", "school": False, "role": "studients_plus"}, 
            {"key": "treasures", "text": "Tesoros de la Biblia", "state": "normal", "school": False, "role": "ministerials"},
            {"key": "pearls", "text": "Busquemos Perlas Escondidas", "state": "normal", "school": False, "role": "ministerials"},
            {"key": "read_bible","text": "Lectura de la Biblia", "state": "normal", "school": False, "role": "studients"},
            {"key": "school_1", "text": "Escuela Asignación 1", "state": "normal", "school": True, "role": "studients", "default": "Empiece conversaciones"},
            {"key": "school_2", "text": "Escuela Asignación 2", "state": "normal", "school": True, "role": "studients", "default": "Haga revisitas"},
            {"key": "school_3", "text": "Escuela Asignación 3", "state": "normal", "school": True, "role": "studients", "default": "Haga discípulos"},
            {"key": "school_4", "text": "Escuela Asignación 4", "state": "normal", "school": True, "role": "studients", "default": "Discurso estudiantil"},
            {"key": "random_1", "text": "Asignación 1", "state": "normal", "school": False, "role": "ministerials"},
            {"key": "random_2", "text": "Asignación 2", "state": "normal", "school": False, "role": "ministerials"},
            {"key": "book", "text": "Estudio Biblico de Congregación", "state": "normal", "school": False, "role": "ministerials"},
            {"key": "read_book", "text": "Lectura en Estudio Biblico", "state": "normal", "school": False, "role": "studients_plus"},
            {"key": "ending_pray", "text": "Oración final", "state": "normal", "school": False, "role": "studients_plus"},
            ]

        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text="", font=("Arial", 16), width=0, state=value["state"], text_color_disabled="#FFFFFF")
                self.widgets["option_type_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], command=self.option_choose_assignation, width=250)
                self.widgets["option_type_" + self.assignations[i]["key"]].set(value["default"])
                self.widgets["option0_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10)
                self.widgets["option_type_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option0_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i, column=3, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)

        self.button_secondary = ctk.CTkButton(master=master, text="Limpiar", width=270, height=40, command=self.clear_widgets)
        self.button_tertiary = ctk.CTkButton(master=master, text="Notificar", width=270, height=40)
        self.button_main = ctk.CTkButton(master=master, text="Generar", width=270, height=40, command=self.generate_replacements)

        self.button_secondary.grid(row=14, column=0, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)
        self.button_tertiary.grid(row=14, column=2, padx=10, pady=(20, 10), sticky="nsew", columnspan=1)
        self.button_main.grid(row=14, column=3, padx=10, pady=(20, 10), sticky="nsew", columnspan=1)

        self.option_choose_assignation(choice="tkOptionMenu")
        self.generate_options()


    def option_choose_participant(self, choice):
        self.witnesses_excluded.append(choice)


    def option_choose_assignation(self, choice):
        for i in range(1, 5):
            option_type = self.widgets[f"option_type_school_{i}"]
            if option_type.get() in ["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias"]:
                self.widgets[f"option1_school_{i}"].grid()
            else:
                self.widgets[f"option1_school_{i}"].grid_remove()
                

    def generate_options(self):
        self.all_witnesses = self.db.read_all_data()
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                which_assignation = school_switcher(self.widgets["option_type_" + self.assignations[i]["key"]].get())
                assignation_options = None
                if which_assignation == "masters":
                    assignation_options = self.all_witnesses["ministerials"]["masters"]
                else:
                    assignation_options = self.all_witnesses[self.assignations[i]["role"]][which_assignation]
                assignation_options = [item[1] for item in assignation_options]
                self.widgets["option0_" + self.assignations[i]["key"]].configure(values=assignation_options)
                self.widgets["option1_" + self.assignations[i]["key"]].configure(values=assignation_options)
                pass
            else:
                assignation_options = self.all_witnesses[self.assignations[i]["role"]][self.assignations[i]["key"]]
                assignation_options = [item[1] for item in assignation_options]
                self.widgets["option_" + self.assignations[i]["key"]].configure(values=assignation_options)


    def generate_replacements(self):
        self.generate_options()
        witnesses_used = []
        for i, value in enumerate(self.assignations):
            if (self.widgets["checkbox_" + self.assignations[i]["key"]].get() == 1):
                if (value["school"] == True):
                    if self.widgets["option0_" + self.assignations[i]["key"]].get() == "":
                        which_assignation = school_switcher(self.widgets["option_type_" + self.assignations[i]["key"]].get())
                        posible_participants = None
                        if which_assignation == "masters":
                            posible_participants = self.all_witnesses["ministerials"]["masters"]
                        else:
                            posible_participants = self.all_witnesses[self.assignations[i]["role"]][which_assignation]
                        choosen_witnesses = self.choose_participant(posible_participants, witnesses_used)
                        choosen_companion = None
                        if which_assignation in ["first", "revisit", "course", "explain"]:
                            gender = choosen_witnesses[3]
                            possible_companion = self.all_witnesses[self.assignations[i]["role"]]
                            choosen_companion = self.choose_companion(gender, possible_companion, witnesses_used)

                        if choosen_witnesses != None:
                            self.widgets["option0_" + self.assignations[i]["key"]].set(choosen_witnesses[1])
                        if choosen_companion != None:
                            self.widgets["option1_" + self.assignations[i]["key"]].set(choosen_companion[1])

                else:
                    if self.widgets["option_" + self.assignations[i]["key"]].get() == "":
                        posible_participants = self.all_witnesses[self.assignations[i]["role"]][self.assignations[i]["key"]]
                        choosen_witnesses = self.choose_participant(posible_participants, witnesses_used)

                        if choosen_witnesses != None:
                            self.widgets["option_" + self.assignations[i]["key"]].set(choosen_witnesses[1])
                        else:
                            self.widgets["option_" + self.assignations[i]["key"]].set("")
                

    def choose_participant(self, posible_participants, witnesses_used):
        for witness in posible_participants:
            if witness[0] not in witnesses_used and witness[1] not in self.witnesses_excluded:
                witnesses_used.append(witness[0])
                return witness
        return None
    

    def choose_companion(self, gender, possible_companion, witnesses_used):
        posible_companions = None
        if gender == "Mujer":
            posible_companions = possible_companion["companion_female"]
        else:
            posible_companions = possible_companion["companion_male"]
        for witness in posible_companions:
            if witness[0] not in witnesses_used and witness[1] not in self.witnesses_excluded:
                witnesses_used.append(witness[0])
                return witness
        return None
    

    def clear_widgets(self):
        self.generate_options()
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["checkbox_" + self.assignations[i]["key"]].deselect()
                self.widgets["option0_" + self.assignations[i]["key"]].set("")
                self.widgets["option1_" + self.assignations[i]["key"]].set("")
            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]].deselect()
                self.widgets["option_" + self.assignations[i]["key"]].set("")