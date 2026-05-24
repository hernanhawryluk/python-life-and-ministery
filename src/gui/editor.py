import datetime
from os import path
import customtkinter as ctk
from src.database import DataBase
from src.scheduler.validation import validate_assignments
from src.gui.dialogs import MessageDialog
from src.utils.switchers import assignment_label, school_switcher


class EditorFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.db = DataBase()
        self.widgets = {}
        self.selected_week_label = None
        self.selected_week_start = None
        self.school_counter = 0
        self.assignations = [
            {"key": "presidency", "text": "Presidencia", "school": False, "role": "elders"},
            {"key": "initial_pray","text": "Oración inicial", "school": False, "role": "studients_plus"},
            {"key": "treasures", "text": "Tesoros de la Biblia", "school": False, "role": "ministerials"},
            {"key": "pearls", "text": "Busquemos Perlas Escondidas", "school": False, "role": "ministerials"},
            {"key": "read_bible","text": "Lectura de la Biblia", "school": False, "role": "studients"},
            {"key": "school_1", "text": "Empiece conversaciones", "school": True, "role": "studients"},
            {"key": "school_2", "text": "Haga revisitas", "school": True, "role": "studients"},
            {"key": "school_3", "text": "Haga discípulos", "school": True, "role": "studients"},
            {"key": "school_4", "text": "Discurso estudiantil", "school": True, "role": "studients"},
            {"key": "random_1", "text": "Asignación 1", "school": False, "role": "ministerials"},
            {"key": "random_2", "text": "Asignación 2", "school": False, "role": "ministerials"},
            {"key": "needs", "text": "Necesidades Locales", "school": False, "role": "elders"},
            {"key": "book", "text": "Estudio Biblico de Congregación", "school": False, "role": "ministerials"},
            {"key": "read_book", "text": "Lectura en Estudio Biblico", "school": False, "role": "studients_plus"},
            {"key": "ending_pray", "text": "Oración final", "school": False, "role": "studients_plus"},
        ]

        self.option_week = ctk.CTkOptionMenu(master=master, values=["Elegir semana"], width=590, height=40, command=self.load_week)
        self.button_save = ctk.CTkButton(master=master, text="Guardar Cambios", width=270, height=40, command=self.save_week)
        self.option_week.grid(row=0, column=0, padx=10, pady=(20, 10), columnspan=2)
        self.button_save.grid(row=0, column=2, padx=10, pady=(20, 10))

        for i, item in enumerate(self.assignations, start=1):
            key = item["key"]
            if item["school"]:
                self.widgets["option_type_" + key] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias", "Discurso estudiantil", "Análisis con el auditorio"], width=250, command=lambda _, k=key: self.update_school_options(k))
                self.widgets["option0_" + key] = ctk.CTkOptionMenu(master=master, values=[""], width=270, command=lambda choice, k=key: self.update_companion_options(k, choice))
                self.widgets["option1_" + key] = ctk.CTkOptionMenu(master=master, values=[""], width=270)
                self.widgets["option_type_" + key].set(item["text"])
                self.widgets["option_type_" + key].grid(row=i, column=0, padx=10, pady=8)
                self.widgets["option0_" + key].grid(row=i, column=1, padx=10, pady=8)
                self.widgets["option1_" + key].grid(row=i, column=2, padx=10, pady=8)
            else:
                self.widgets["label_" + key] = ctk.CTkLabel(master=master, text=item["text"], width=300, anchor="w", font=("Arial", 15))
                self.widgets["option_" + key] = ctk.CTkOptionMenu(master=master, values=[""], width=270)
                self.widgets["label_" + key].grid(row=i, column=0, padx=10, pady=8)
                self.widgets["option_" + key].grid(row=i, column=1, padx=10, pady=8)

        self.label_status = ctk.CTkLabel(master=master, text="", width=860, anchor="w", text_color="#D65A5A")
        self.label_status.grid(row=16, column=0, padx=10, pady=10, columnspan=3, sticky="w")

        self.generate_options()
        self.load_weeks()

    def load_weeks(self):
        weeks = self.db.read_meeting_weeks()
        self.option_week.configure(values=weeks)
        if weeks:
            self.option_week.set("Elegir semana")

    def generate_options(self):
        self.all_witnesses = self.db.read_data_for_assignations()
        for item in self.assignations:
            key = item["key"]
            if item["school"]:
                self.update_school_options(key)
            else:
                options = [row[1] for row in self.all_witnesses[item["role"]][key]]
                self.widgets["option_" + key].configure(values=options)

    def update_school_options(self, key):
        assignment = school_switcher(self.widgets["option_type_" + key].get())
        if assignment == "masters":
            options = [row[1] for row in self.all_witnesses["ministerials"]["masters"]]
        else:
            options = [row[1] for row in self.all_witnesses["studients"][assignment]]
        companions = [row[1] for row in self.all_witnesses["studients"]["companion_female"] + self.all_witnesses["studients"]["companion_male"]]
        self.widgets["option0_" + key].configure(values=options)
        self.widgets["option1_" + key].configure(values=companions)

    def update_companion_options(self, key, titular):
        if not titular:
            return
        assignment = school_switcher(self.widgets["option_type_" + key].get())
        if assignment not in ["first", "revisit", "course", "explain"]:
            self.widgets["option1_" + key].set("")
            return
        witness = self.db.read_participant(titular)
        if not witness:
            return
        companion_key = "companion_female" if witness[0][3] == "Mujer" else "companion_male"
        options = [row[1] for row in self.all_witnesses["studients"][companion_key] if row[1] != titular]
        self.widgets["option1_" + key].configure(values=options)

    def load_week(self, week_label):
        self.clear_widgets()
        self.selected_week_label = week_label
        self.selected_week_start = self.db.meeting_week_start(week_label)
        self.school_counter = 0
        for assignment_type, label, titular, companion in self.db.read_meeting_assignments(week_label):
            if assignment_type in ["first", "revisit", "course", "explain", "speech", "masters"]:
                self.school_counter += 1
                key = f"school_{self.school_counter}"
                if "option_type_" + key in self.widgets:
                    self.widgets["option_type_" + key].set(label)
                    self.widgets["option0_" + key].set(titular)
                    self.widgets["option1_" + key].set(companion or "")
                    self.update_companion_options(key, titular)
            else:
                self.widgets["option_" + assignment_type].set(titular)
        self.label_status.configure(text="")

    def clear_widgets(self):
        for item in self.assignations:
            key = item["key"]
            if item["school"]:
                self.widgets["option_type_" + key].set(item["text"])
                self.widgets["option0_" + key].set("")
                self.widgets["option1_" + key].set("")
            else:
                self.widgets["option_" + key].set("")

    def save_week(self):
        if not self.selected_week_label or not self.selected_week_start:
            self.label_status.configure(text="Elegí una semana para editar.")
            return
        data = self.collect_data()
        errors = validate_assignments(data, self.db)
        if errors:
            self.label_status.configure(text=errors[0])
            MessageDialog(self, "Revisar asignaciones", errors)
            return
        self.db.update_meeting(self.selected_week_label, data)
        self.rewrite_log()
        self.label_status.configure(text="Cambios guardados.")

    def collect_data(self):
        data = []
        week = datetime.date.fromisoformat(self.selected_week_start)
        for item in self.assignations:
            key = item["key"]
            if item["school"]:
                titular = self.widgets["option0_" + key].get()
                if titular:
                    assignment = school_switcher(self.widgets["option_type_" + key].get())
                    companion = self.widgets["option1_" + key].get()
                    data.append([assignment, titular, week, companion] if companion else [assignment, titular, week])
            else:
                titular = self.widgets["option_" + key].get()
                if titular:
                    data.append([key, titular, week])
        return data

    def rewrite_log(self):
        file_path = path.join("data", "meetings.log")
        report = self.db.read_meeting_report(self.selected_week_label)
        if not path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("-------------------------------\n" + report + "\n")
            return
        with open(file_path, "r") as file:
            content = file.read()
        start = content.find(self.selected_week_label)
        if start == -1:
            with open(file_path, "a") as file:
                file.write("-------------------------------\n" + report + "\n")
            return
        separator = content.find("-------------------------------", start)
        end = len(content) if separator == -1 else separator
        new_content = content[:start] + report + "\n" + content[end:]
        with open(file_path, "w") as file:
            file.write(new_content)
