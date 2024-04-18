import customtkinter as ctk
import calendar
import datetime

class MeetingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.weeks = self.weeks()
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

        self.buttonGenerate = ctk.CTkButton(master=master, text="Nueva Semana", width=300, height=40)
        self.entryWeek = ctk.CTkEntry(master=master, width=270, height=40)
        print(self.weeks[0])
        self.entryWeek.insert(0, self.weeks[0])
        self.buttonSave = ctk.CTkButton(master=master, text="Guardar Semana", width=270, height=40)

        self.buttonGenerate.grid(row=14, column=0, padx=10, pady=(20, 10),columnspan=2)
        self.entryWeek.grid(row=14, column=2, padx=10, pady=(20, 10))
        self.buttonSave.grid(row=14, column=3, padx=10, pady=(20, 10), columnspan=1)

    def weeks(self):
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        months_in_spansh = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]

        if current_month == 12:
            next_year = current_year + 1
            next_month = 1
        else:
            next_year = current_year
            next_month = current_month + 1

        first_day_next_month = datetime.date(next_year, next_month, 1)
        first_monday = first_day_next_month + datetime.timedelta(days=(0 - first_day_next_month.weekday()) % 7)
        days_in_the_month = calendar.monthrange(next_year, next_month)[1]

        weeks = []

        start_of_week = first_monday
        for day in range(first_monday.day, days_in_the_month + 1):
            date = datetime.date(next_year, next_month, day)
            if date.weekday() == 0:
                start_of_week = date
            if date.weekday() == 6 or day == days_in_the_month:
                end_of_week = date
                weeks.append((start_of_week, end_of_week))
                start_of_week = None

        last_week = weeks[-1]
        last_monday_of_the_month = last_week[0]
        weeks[-1] = (last_monday_of_the_month, last_monday_of_the_month + datetime.timedelta(days=6))
        
        formatted_weeks = []
        for i, week in enumerate(weeks, start=1):
            current_month = months_in_spansh[week[0].month - 1]
            if week[0].day < week[1].day:
                formatted_weeks.append(f"Semana del {week[0].day} - {week[1].day} de {current_month.capitalize()}")
            else:
                if (week[1].month == 12):
                    next_month = months_in_spansh[0]
                else:
                    next_month = months_in_spansh[week[0].month + 1]
                formatted_weeks.append(f"Semana del {week[0].day} de {current_month.capitalize()} - {week[1].day} de {next_month.capitalize()}")
        
        return formatted_weeks