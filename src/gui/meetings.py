import customtkinter as ctk
from os import path
from src.database import DataBase
from src.utils.weeks import calculate_weeks
from src.utils.switchers import school_switcher, meeting_switcher

class MeetingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.generated_months = 0
        self.weeks = calculate_weeks(self.generated_months)
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
                self.widgets["option_type_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], command=self.option_choose_assignation, width=250)
                self.widgets["option_type_" + self.assignations[i]["key"]].set(value["text"])
                self.widgets["option0_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10)
                self.widgets["option_type_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option0_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i, column=3, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                if (value["checked_box"] == True):
                    self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=self.option_choose_participant, width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)

        self.secondary_button = ctk.CTkButton(master=master, text="Saltar Semana", width=300, height=40, command=self.secondary_button_action)
        self.label_week = ctk.CTkLabel(master=master, text=self.weeks[0], width=270, height=40)
        self.main_button = ctk.CTkButton(master=master, text="Generar Semana", width=270, height=40, command=self.main_button_action)

        self.secondary_button.grid(row=15, column=0, padx=10, pady=(20, 10),columnspan=2)
        self.label_week.grid(row=15, column=2, padx=10, pady=(20, 10))
        self.main_button.grid(row=15, column=3, padx=10, pady=(20, 10), columnspan=1)

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
        self.generate_options()


    def secondary_button_action(self):
        if self.secondary_button.cget("text") == "Saltar Semana":
            self.main_button.configure(text="Generar Semana")
            self.skip_week()
        elif (self.secondary_button.cget("text") == "Cancelar"):
            self.main_button.configure(text="Generar Semana")
            self.secondary_button.configure(text="Saltar Semana")
            self.clear_widgets()


    def main_button_action(self):
        if self.main_button.cget("text") == "Generar Semana":
            self.main_button.configure(text="Guardar Semana")
            self.secondary_button.configure(text="Cancelar")
            self.generate_week()
        else:
            self.main_button.configure(text="Generar Semana")
            self.secondary_button.configure(text="Saltar Semana")
            self.save_week()


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


    def generate_week(self):
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

    def skip_week(self):
        self.weeks.pop(0)
        if self.weeks == []:
            self.generated_months += 1
            self.weeks = calculate_weeks(self.generated_months)
        self.label_week.configure(text=self.weeks[0])
        self.witnesses_excluded = []
        self.clear_widgets()

    def clear_widgets(self):
        self.generate_options()
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["option_type_" + self.assignations[i]["key"]].set(self.assignations[i]["text"])
                self.widgets["option0_" + self.assignations[i]["key"]].set("")
                self.widgets["option1_" + self.assignations[i]["key"]].set("")
                if self.assignations[i]["checked_box"] == True:
                    self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                else:
                    self.widgets["checkbox_" + self.assignations[i]["key"]].deselect()
            else:
                self.widgets["option_" + self.assignations[i]["key"]].set("")
                if self.assignations[i]["checked_box"] == True:
                    self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                else:
                    self.widgets["checkbox_" + self.assignations[i]["key"]].deselect()

    def save_week(self):
        self.write_to_file("--------------------------------------------")
        self.write_to_file(self.label_week.cget("text"))
        self.write_to_file("--------------------------------------------\n")
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                checkbox = self.widgets["checkbox_" + self.assignations[i]["key"]].get()
                if checkbox:
                    assignation = self.widgets["option_type_" + self.assignations[i]["key"]].get()    
                    assigned = self.widgets["option0_" + self.assignations[i]["key"]].get()
                    assistant = self.widgets["option1_" + self.assignations[i]["key"]].get()
                    self.write_to_file(assignation + ": " + assigned + " - " + assistant)
            else:
                assignation = self.widgets["checkbox_" + self.assignations[i]["key"]].cget("text")
                assigned = self.widgets["option_" + self.assignations[i]["key"]].get()
                self.write_to_file(assignation + ": " + assigned)
        self.write_to_file("\n\n")

        data_dict = []
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                checkbox = self.widgets["checkbox_" + self.assignations[i]["key"]].get()
                if checkbox:
                    assignation = self.widgets["option_type_" + self.assignations[i]["key"]].get()
                    assignation = school_switcher(assignation)
                    assigned = self.widgets["option0_" + self.assignations[i]["key"]].get()
                    assistant = self.widgets["option1_" + self.assignations[i]["key"]].get()
                    data_dict.append([assignation, assigned, assistant])
                    
            else:
                assignation = self.widgets["checkbox_" + self.assignations[i]["key"]].cget("text")
                assignation = meeting_switcher(assignation)
                assigned = self.widgets["option_" + self.assignations[i]["key"]].get()
                data_dict.append([assignation, assigned])

        self.db.write_data(data_dict)
        self.skip_week()
            

    def write_to_file(self, text):
        file = path.join("data", "reuniones.txt")
        with open(file, 'a') as archivo:
            archivo.write(text + "\n")


        
        