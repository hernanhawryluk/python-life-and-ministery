import customtkinter as ctk
from src.database import DataBase
from src.utils.switchers import school_switcher, meeting_switcher
from os import path

class NotificationsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.school_counter = 0
        self.loaded_weeks = 0
        self.generated_months = 0
        self.db = DataBase()
        self.witnesses_excluded = []
        self.assignations = []

        self.button_load_file = ctk.CTkButton(master=master, text="Cargar Archivo", width=400, height=40, command=self.read_file)
        self.label_arrow = ctk.CTkLabel(master=master, text="►", width=10, height=40)
        self.button_open_whatsapp = ctk.CTkButton(master=master, text="Abrir WhatsApp Web", width=400, height=40)
        self.label_weeks = ctk.CTkLabel(master=master, text="Seleccionar notificaciones a enviar: ", font=("Arial", 19), width=250, height=40)
        self.label_arrow_down = ctk.CTkLabel(master=master, text="▼", width=10, height=40)

        self.button_load_file.grid(row=0, column=0, padx=10, pady=(20, 10))
        self.label_arrow.grid(row=0, column=1, padx=10, pady=(20, 10))
        self.button_open_whatsapp.grid(row=0, column=2, padx=10, pady=(20, 10))
        
        self.label_weeks.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.label_arrow_down.grid(row=1, column=2, padx=10, pady=(0,10))

        self.frame = ctk.CTkScrollableFrame(master=master, width=920, height=240)
        self.frame.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        self.button_open_show_weeks = ctk.CTkButton(master=master, text="Enviar Notificaciones", width=910, height=40)
        self.button_open_show_weeks.grid(row=3, column=0, padx=10, pady=(20, 10), columnspan=3)
        
    
    def main_button_action(self):
        pass

    def secondary_button_action(self):
        self.read_file()

    def fill_options(self, line):
        assignation = ""
        name = ""
        companion = ""
        line = line.replace("\n", "")
        parts = line.split(": ")
        assignation_part = parts[0]
        name_part = parts[1]
        if assignation_part in ["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias", "Discurso estudiantil", "Análisis con el auditorio"]:
            self.school_counter += 1
            assignation = assignation_part
            name_part = name_part.split(" - ")
            name = name_part[0]
            companion = name_part[1]
            print("assignation: " + assignation + " name: " + name + " companion: " + companion)
        else:
            assignation = meeting_switcher(assignation_part)
            name = name_part
            print("assignation: " + assignation + " name: " + name)


    def read_file(self):
        file_path = path.join("data", "meetings.log")
        if (path.exists(file_path) == True):
            with open(file_path, 'r') as file:
                filling_activated = False
                for line in file:
                    if line == "-------------------------------\n":
                        pass
                    elif filling_activated == True:
                        if line[:6] == "Semana":
                            column = ((self.loaded_weeks - 1) % 3)
                            if self.loaded_weeks % 3 == 0 and self.loaded_weeks != 0:
                                self.widgets["week_" + str(self.loaded_weeks)] = ctk.CTkCheckBox(master=self.frame, text=line, width=280, fg_color="#555555")
                                self.widgets["week_" + str(self.loaded_weeks)].grid(row=self.loaded_weeks // 3, column=column, padx=10, pady=10)
                            else:
                                self.widgets["week_" + str(self.loaded_weeks)] = ctk.CTkCheckBox(master=self.frame, text=line, width=280, fg_color="#555555")
                                self.widgets["week_" + str(self.loaded_weeks)].grid(row=self.loaded_weeks // 3, column=column, padx=10, pady=10)
                            self.loaded_weeks += 1
                        elif line == "Notificated: True\n":
                            filling_activated = False
                        elif line == "Notificated: False\n":
                            pass
                        else: 
                            self.fill_options(line)
                    elif line == "Notificated: False\n":
                            filling_activated = True
                self.school_counter = 0

    def button_week(self, week):
        print(week)

    def set_notified(self):
        modified_once = False
        file_path = path.join("data", "meetings.log")
        if (path.exists(file_path) == True):
            with open(file_path, 'r') as file:
                lines = file.readlines()
            with open(file_path, 'w') as file:
                for line in lines:
                    if modified_once == False and line == "Notificated: False\n":
                            file.write("Notificated: True\n")
                            modified_once = True
                    else:
                        file.write(line)

    def send_notifications(self):
        pass