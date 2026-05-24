import customtkinter as ctk
import threading
from os import path
from src.database import DataBase
from src.utils.weeks import calculate_weeks, format_week
from src.utils.switchers import school_switcher, meeting_switcher
from src.utils.meeting_program import fetch_week_program
from src.scheduler.validation import validate_assignments
from src.gui.assignment_helpers import collect_week_data, write_week_log
from src.gui.dialogs import MessageDialog

class ManualFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.generated_months = 0
        self.weeks = calculate_weeks()
        self.db = DataBase()
        self.witnesses_excluded = []
        self.program_loaded_week = None
        self.program_loading_week = None
        self.assignations = [
            {"key": "presidency", "text": "Presidencia", "state": "normal", "checked_box": True, "school": False, "role": "elders"},
            {"key": "initial_pray","text": "Oración inicial", "state": "normal", "checked_box": True, "school": False, "role": "studients_plus"}, 
            {"key": "treasures", "text": "Tesoros de la Biblia", "state": "normal", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "pearls", "text": "Busquemos Perlas Escondidas", "state": "normal", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "read_bible","text": "Lectura de la Biblia", "state": "normal", "checked_box": True, "school": False, "role": "studients"},
            {"key": "school_1", "text": "Empiece conversaciones", "state": "normal", "checked_box": True, "school": True, "role": "studients"},
            {"key": "school_2", "text": "Haga revisitas", "state": "normal", "checked_box": True, "school": True, "role": "studients"},
            {"key": "school_3", "text": "Haga discípulos", "state": "normal", "checked_box": True, "school": True, "role": "studients"},
            {"key": "school_4", "text": "Discurso estudiantil", "state": "normal", "checked_box": False, "school": True, "role": "studients"},
            {"key": "random_1", "text": "Asignación 1", "state": "normal", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "random_2", "text": "Asignación 2", "state": "normal", "checked_box": False, "school": False, "role": "ministerials"},
            {"key": "needs", "text": "Necesidades Locales", "state": "normal", "checked_box": False, "school": False, "role": "elders"},
            {"key": "book", "text": "Estudio Biblico de Congregación", "state": "normal", "checked_box": True, "school": False, "role": "ministerials"},
            {"key": "read_book", "text": "Lectura en Estudio Biblico", "state": "normal", "checked_box": True, "school": False, "role": "studients_plus"},
            {"key": "ending_pray", "text": "Oración final", "state": "normal", "checked_box": True, "school": False, "role": "studients_plus"},
            ]
        
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text="", font=("Arial", 16), width=0, state=value["state"], text_color_disabled="#FFFFFF")
                if (value["checked_box"] == True):
                    self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_type_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], command=self.option_choose_assignation, width=250)
                self.widgets["option_type_" + self.assignations[i]["key"]].set(value["text"])
                self.widgets["option0_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=lambda choice, key=self.assignations[i]["key"], field="option0": self.option_choose_participant(choice, key, field), width=270)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=lambda choice, key=self.assignations[i]["key"], field="option1": self.option_choose_participant(choice, key, field), width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, padx=10, pady=10)
                self.widgets["option_type_" + self.assignations[i]["key"]].grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option0_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i, column=3, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                if (value["checked_box"] == True):
                    self.widgets["checkbox_" + self.assignations[i]["key"]].select()
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], command=lambda choice, key=self.assignations[i]["key"], field="option": self.option_choose_participant(choice, key, field), width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i, column=2, padx=10, pady=10)

        self.secondary_button = ctk.CTkButton(master=master, text="Saltar", width=300, height=40, command=self.secondary_button_action)
        self.label_week = ctk.CTkLabel(master=master, text=format_week(self.weeks[0]), width=270, height=40)
        self.main_button = ctk.CTkButton(master=master, text="Guardar", width=270, height=40, command=self.main_button_action)
        self.program_button = ctk.CTkButton(master=master, text="Cargar programa", width=300, height=36, command=self.force_week_program)
        self.label_reason = ctk.CTkLabel(master=master, text="", width=520, height=28, anchor="w")
        self.label_validation = ctk.CTkLabel(master=master, text="", width=860, height=28, anchor="w", text_color="#D65A5A")

        self.secondary_button.grid(row=15, column=0, padx=10, pady=(20, 10),columnspan=2)
        self.label_week.grid(row=15, column=2, padx=10, pady=(20, 10))
        self.main_button.grid(row=15, column=3, padx=10, pady=(20, 10), columnspan=1)
        self.program_button.grid(row=16, column=0, padx=10, pady=(0, 8), columnspan=2)
        self.label_reason.grid(row=16, column=2, padx=10, pady=(0, 8), columnspan=2, sticky="w")
        self.label_validation_grid = {"row": 17, "column": 0, "padx": 10, "pady": (0, 10), "columnspan": 4, "sticky": "w"}

        self.option_choose_assignation(choice="tkOptionMenu")
        self.generate_options()


    def option_choose_participant(self, choice, key=None, field=None):
        if choice and choice not in self.witnesses_excluded:
            self.witnesses_excluded.append(choice)
        if choice and field in ["option", "option0"] and key is not None:
            self.show_assignment_reason(key, choice)
        if field == "option0" and key is not None:
            self.update_companion_options(key, choice)

    def show_assignment_reason(self, key, name):
        if key.startswith("school_"):
            assignment = school_switcher(self.widgets["option_type_" + key].get())
        else:
            assignment = key
        self.label_reason.configure(text=self.db.assignment_summary(name, assignment))


    def option_choose_assignation(self, choice):
        self.generate_options()
        for i in range(1, 5):
            option_type = self.widgets[f"option_type_school_{i}"]
            if option_type.get() in ["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias"]:
                self.widgets[f"option1_school_{i}"].grid()
                titular = self.widgets[f"option0_school_{i}"].get()
                if titular:
                    self.update_companion_options(f"school_{i}", titular)
            else:
                self.widgets[f"option1_school_{i}"].set("")
                self.widgets[f"option1_school_{i}"].grid_remove()


    def secondary_button_action(self):
        self.skip_week()

    def main_button_action(self):
        self.save_week()


    def generate_options(self):
        self.all_witnesses = self.db.read_data_for_simplified_assignations()
        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                which_assignation = school_switcher(self.widgets["option_type_" + self.assignations[i]["key"]].get())
                assignation_options = None
                companion_options = self.all_witnesses["studients"]["companion_female"] + self.all_witnesses["studients"]["companion_male"]
                if which_assignation == "masters":
                    assignation_options = self.all_witnesses["ministerials"]["masters"]
                else:
                    assignation_options = self.all_witnesses[self.assignations[i]["role"]][which_assignation]
                assignation_options = [item[1] for item in assignation_options]
                companion_options = [item[1] for item in companion_options]
                self.widgets["option0_" + self.assignations[i]["key"]].configure(values=assignation_options)
                self.widgets["option1_" + self.assignations[i]["key"]].configure(values=companion_options)
                pass
            else:
                assignation_options = self.all_witnesses[self.assignations[i]["role"]][self.assignations[i]["key"]]
                assignation_options = [item[1] for item in assignation_options]
                self.widgets["option_" + self.assignations[i]["key"]].configure(values=assignation_options)

    def update_companion_options(self, key, titular):
        if not titular:
            return
        option_type = self.widgets["option_type_" + key].get()
        if option_type not in ["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias"]:
            self.widgets["option1_" + key].set("")
            return
        witness_data = self.db.read_participant(titular)
        if not witness_data:
            return
        gender = witness_data[0][3]
        companion_key = "companion_female" if gender == "Mujer" else "companion_male"
        companion_options = [
            item[1]
            for item in self.all_witnesses["studients"][companion_key]
            if item[1] != titular
        ]
        self.widgets["option1_" + key].configure(values=companion_options)
        if self.widgets["option1_" + key].get() not in companion_options:
            self.widgets["option1_" + key].set("")
                
    def choose_participant(self, posible_participants):
        for witness in posible_participants:
            if witness[1] not in self.witnesses_excluded:
                self.witnesses_excluded.append(witness[1])
                return witness
        return None
    
    def choose_companion(self, gender, possible_companion):
        posible_companions = None
        if gender == "Mujer":
            posible_companions = possible_companion["companion_female"]
        else:
            posible_companions = possible_companion["companion_male"]
        for witness in posible_companions:
            if witness[1] not in self.witnesses_excluded:
                self.witnesses_excluded.append(witness[1])
                return witness
        return None

    def skip_week(self):
        self.weeks.pop(0)
        if self.weeks == []:
            self.generated_months += 1
            self.weeks = calculate_weeks(self.generated_months)
        self.label_week.configure(text=format_week(self.weeks[0]))
        self.witnesses_excluded = []
        self.hide_validation()
        self.label_reason.configure(text="")
        self.clear_widgets()
        self.generate_options()
        self.apply_week_program()

    def ensure_week_program(self):
        week = self.weeks[0][0]
        if self.program_loaded_week != week:
            self.apply_week_program()

    def force_week_program(self):
        self.program_loaded_week = None
        self.apply_week_program()

    def apply_week_program(self):
        week = self.weeks[0][0]
        if self.program_loading_week == week:
            return
        self.program_loading_week = week
        self.program_button.configure(state="disabled", text="Cargando...")
        self.label_reason.configure(text="Cargando programa semanal desde WOL...")
        self.hide_validation()
        threading.Thread(target=self.fetch_week_program_background, args=(week,), daemon=True).start()

    def fetch_week_program_background(self, week):
        program = fetch_week_program(week)
        self.after(0, lambda: self.apply_week_program_result(week, program))

    def apply_week_program_result(self, week, program):
        self.program_loading_week = None
        self.program_button.configure(state="normal", text="Cargar programa")
        if week != self.weeks[0][0]:
            return
        if not program["ok"]:
            self.show_validation(f"No se pudo obtener el programa semanal; se usan valores manuales. {program['error']}")
            return
        self.program_loaded_week = week
        self.label_reason.configure(text=f"Programa cargado desde: {program['url']}")
        self.hide_validation()
        assignments = program["school_assignments"]
        for index in range(1, 5):
            key = f"school_{index}"
            checkbox = self.widgets["checkbox_" + key]
            if index <= len(assignments):
                checkbox.select()
                self.widgets["option_type_" + key].set(assignments[index - 1])
            else:
                checkbox.deselect()
                self.widgets["option_type_" + key].set(self.assignations[index + 4 - 1]["text"])
                self.widgets["option0_" + key].set("")
                self.widgets["option1_" + key].set("")
        self.apply_life_program(program["life_assignments"])
        self.option_choose_assignation(choice="program")

    def show_validation(self, text):
        self.label_validation.configure(text=text)
        self.label_validation.grid(**self.label_validation_grid)

    def hide_validation(self):
        self.label_validation.grid_remove()

    def apply_life_program(self, life_assignments):
        for key in ["random_1", "random_2", "needs"]:
            if life_assignments.get(key, False):
                self.widgets["checkbox_" + key].select()
            else:
                self.widgets["checkbox_" + key].deselect()
                self.widgets["option_" + key].set("")

    def clear_widgets(self):
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
        data_dict = collect_week_data(self)
        errors = validate_assignments(data_dict, self.db)
        if errors:
            self.show_validation(errors[0])
            MessageDialog(self, "Revisar asignaciones", errors)
            return
        self.hide_validation()
        self.write_week_log()
        self.db.write_data(data_dict, self.label_week.cget("text"))
        self.skip_week()

    def write_week_log(self):
        write_week_log(self)
            

    def write_to_file(self, text):
        file_path = path.join("data", "meetings.log")
        with open(file_path, 'a') as file:
            file.write(text + "\n")


        
        
