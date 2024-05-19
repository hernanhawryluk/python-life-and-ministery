import customtkinter as ctk
from src.database import DataBase
from src.utils.switchers import school_switcher
import datetime

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
            {"key": "needs", "text": "Necesidades Locales", "state": "normal", "checked_box": False, "school": False, "role": "elders"},
            {"key": "book", "text": "Estudio Biblico de Congregación", "state": "normal", "school": False, "role": "ministerials"},
            {"key": "read_book", "text": "Lectura en Estudio Biblico", "state": "normal", "school": False, "role": "studients_plus"},
            {"key": "ending_pray", "text": "Oración final", "state": "normal", "school": False, "role": "studients_plus"},
            ]

        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["option_type_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], command=self.option_choose_assignation, width=250)
                self.widgets["option_type_" + self.assignations[i]["key"]].set(value["default"])
                self.widgets["option0_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)

                self.widgets["option_type_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10, sticky="nsew")
                self.widgets["option0_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10)
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)

            else:
                self.widgets["label_" + self.assignations[i]["key"]] = ctk.CTkLabel(master=master, text=value["text"], font=("Arial", 16), width=300, anchor="w")
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)

                self.widgets["label_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10)

        self.button_secondary = ctk.CTkButton(master=master, text="Limpiar", width=270, height=40, command=self.clear_widgets)
        self.button_main = ctk.CTkButton(master=master, text="Guardar", width=270, height=40, command=self.save_dates)

        self.button_secondary.grid(row=15, column=0, padx=10, pady=(20, 10), sticky="nsew")
        self.button_main.grid(row=15, column=1, padx=10, pady=(20, 10), sticky="nsew", columnspan=2)

        self.option_choose_assignation(choice="tkOptionMenu")
        self.generate_options()


    def option_choose_participant(self, choice):
        self.witnesses_excluded.append(choice)


    def save_dates(self):
        data_dict = []
        week = datetime.date.today().strftime('%Y-%m-%d')
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                assigned = self.widgets["option0_" + self.assignations[i]["key"]].get()
                assistant = self.widgets["option1_" + self.assignations[i]["key"]].get()
                if assigned != "":
                    data_dict.append(["replacements_date", assigned, week])
                elif assistant != "":
                    data_dict.append(["replacements_date", assistant, week])
            else:
                assigned = self.widgets["option_" + self.assignations[i]["key"]].get()
                if assigned != "":
                    data_dict.append(["replacements_date", assigned, week])
        self.db.write_data(data_dict)


    def option_choose_assignation(self, choice):
        for i in range(1, 5):
            option_type = self.widgets[f"option_type_school_{i}"]
            if option_type.get() in ["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias"]:
                self.widgets[f"option1_school_{i}"].grid()
            else:
                self.widgets[f"option1_school_{i}"].grid_remove()
        self.generate_options()
                

    def generate_options(self):
        self.all_witnesses = self.db.read_data_for_assignations(replacements = True)
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
    

    def clear_widgets(self):
        self.generate_options()
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["option0_" + self.assignations[i]["key"]].set("")
                self.widgets["option1_" + self.assignations[i]["key"]].set("")
            else:
                self.widgets["option_" + self.assignations[i]["key"]].set("")