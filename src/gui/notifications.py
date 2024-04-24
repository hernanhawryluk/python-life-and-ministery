import customtkinter as ctk
from src.database import DataBase
from src.utils.switchers import school_switcher
from src.utils.weeks import format_week
import datetime

class NotificationsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.generated_months = 0
        self.db = DataBase()
        self.witnesses_excluded = []
        self.assignations = [
            {"key": "presidency", "text": "Presidencia", "state": "disabled", "checked_box": True, "school": False, "role": "elders"},
            {"key": "initial_pray","text": "Oración inicial", "state": "disabled", "checked_box": True, "school": False, "role": "studients_plus"}, 
            {"key": "treasures", "text": "Tesoros de la Biblia", "state": "disabled", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "pearls", "text": "Busquemos Perlas Escondidas", "state": "disabled", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "read_bible","text": "Lectura de la Biblia", "state": "disabled", "checked_box": True, "school": False, "role": "studients"},
            {"key": "school_1", "text": "Empiece conversaciones", "state": "normal", "checked_box": True, "school": True, "role": "studients"},
            {"key": "school_2", "text": "Haga revisitas", "state": "normal", "checked_box": True, "school": True, "role": "studients"},
            {"key": "school_3", "text": "Haga discípulos", "state": "normal", "checked_box": True, "school": True, "role": "studients"},
            {"key": "school_4", "text": "Discurso estudiantil", "state": "normal", "checked_box": False, "school": True, "role": "studients"},
            {"key": "random_1", "text": "Asignación 1", "state": "normal", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "random_2", "text": "Asignación 2", "state": "normal", "checked_box": False, "school": False, "role": "ministerials"},
            {"key": "needs", "text": "Necesidades Locales", "state": "normal", "checked_box": False, "school": False, "role": "elders"},
            {"key": "book", "text": "Estudio Biblico de Congregación", "state": "normal", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "read_book", "text": "Lectura en Estudio Biblico", "state": "normal", "checked_box": True, "school": False, "role": "studients_plus"},
            {"key": "ending_pray", "text": "Oración final", "state": "disabled", "checked_box": True, "school": False, "role": "studients_plus"},
            ]
        
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text="", font=("Arial", 16), width=0, state=value["state"], text_color_disabled="#FFFFFF")
                if (value["checked_box"] == True):
                    self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_type_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], width=250)
                self.widgets["option_type_" + self.assignations[i]["key"]].set(value["text"])
                self.widgets["option0_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=270)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10)
                self.widgets["option_type_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option0_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i, column=3, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                if (value["checked_box"] == True):
                    self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)

        self.secondary_button = ctk.CTkButton(master=master, text="Siguiente", width=300, height=40, command=self.secondary_button_action)
        self.label_week = ctk.CTkLabel(master=master, text="Sin asignaciones para notificar", width=270, height=40)
        self.main_button = ctk.CTkButton(master=master, text="Notificar", width=270, height=40, command=self.main_button_action)

        self.secondary_button.grid(row=15, column=0, padx=10, pady=(20, 10),columnspan=2)
        self.label_week.grid(row=15, column=2, padx=10, pady=(20, 10))
        self.main_button.grid(row=15, column=3, padx=10, pady=(20, 10), columnspan=1)

        self.generate_options()
    
    def main_button_action(self):
        pass

    def secondary_button_action(self):
        pass

    def generate_options(self):
        self.all_witnesses = self.db.read_data_for_assignations()
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