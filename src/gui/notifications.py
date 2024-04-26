import customtkinter as ctk
from src.database import DataBase
from src.utils.switchers import school_switcher, meeting_switcher
from os import path
import webbrowser
import pyperclip

class NotificationsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        # self.notifications_to_send = []
        # self.school_counter = 0
        # self.loaded_notification = 0
        # self.column = 0
        # self.row = 0
        # self.to_notify = []
        # self.generated_months = 0
        # self.db = DataBase()
        # self.witnesses_excluded = []
        # self.assignations = []
        self.assignations = [
            {"key": "presidency", "text": "Presidencia", "state": "normal", "checked_box": False, "school": False, "role": "elders"},
            {"key": "initial_pray","text": "Oración inicial", "state": "normal", "checked_box": False, "school": False, "role": "studients_plus"}, 
            {"key": "treasures", "text": "Tesoros de la Biblia", "state": "normal", "checked_box": False, "school": False, "role": "ministerials"},
            {"key": "pearls", "text": "Busquemos Perlas Escondidas", "state": "normal", "checked_box": False, "school": False, "role": "ministerials"},
            {"key": "read_bible","text": "Lectura de la Biblia", "state": "normal", "checked_box": False, "school": False, "role": "studients"},
            {"key": "school_1", "text": "Empiece conversaciones", "state": "normal", "checked_box": False, "school": True, "role": "studients"},
            {"key": "school_2", "text": "Haga revisitas", "state": "normal", "checked_box": False, "school": True, "role": "studients"},
            {"key": "school_3", "text": "Haga discípulos", "state": "normal", "checked_box": False, "school": True, "role": "studients"},
            {"key": "school_4", "text": "Discurso estudiantil", "state": "normal", "checked_box": False, "school": True, "role": "studients"},
            {"key": "random_1", "text": "Asignación 1", "state": "normal", "checked_box": False, "school": False, "role": "ministerials"},
            {"key": "random_2", "text": "Asignación 2", "state": "normal", "checked_box": False, "school": False, "role": "ministerials"},
            {"key": "needs", "text": "Necesidades Locales", "state": "normal", "checked_box": False, "school": False, "role": "elders"},
            {"key": "book", "text": "Estudio Biblico de Congregación", "state": "normal", "checked_box": False, "school": False, "role": "ministerials"},
            {"key": "read_book", "text": "Lectura en Estudio Biblico", "state": "normal", "checked_box": False, "school": False, "role": "studients_plus"},
            {"key": "ending_pray", "text": "Oración final", "state": "normal", "checked_box": False, "school": False, "role": "studients_plus"},
            ]
        
        self.button_lead_weeks = ctk.CTkButton(master=master, text="Carga semanas", font=("Arial", 16), width=300, height=36)
        self.option_week_selector = ctk.CTkOptionMenu(master=master, values=["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5"], width=270, height=36)
        self.button_open_whatsapp = ctk.CTkButton(master=master, text="Abrir WhatsApp", font=("Arial", 16), width=270, height=36)
        self.option_week_selector.set("Semana 1")

        self.button_lead_weeks.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.option_week_selector.grid(row=0, column=2, padx=10, pady=10)
        self.button_open_whatsapp.grid(row=0, column=3, padx=10, pady=10)

        self.label_copy = ctk.CTkLabel(master=master, text=" ▼  Copiar al portapapeles", font=("Arial", 18), width=300, anchor="w")
        self.label_copy.grid(row=1, column=0, padx=10, pady=(20, 10), columnspan=2)

        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text="", font=("Arial", 16), width=0, state=value["state"], text_color_disabled="#FFFFFF")
                self.widgets["option_type_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], width=250)
                self.widgets["option_type_" + self.assignations[i]["key"]].set(value["text"])
                self.widgets["option0_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=270)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i + 2, column=0, padx=10, pady=10)
                self.widgets["option_type_" + self.assignations[i]["key"]].grid(row=i + 2, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option0_" + self.assignations[i]["key"]].grid(row=i + 2, column=2, padx=10, pady=10)
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i + 2, column=3, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF")
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=270)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i + 2, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i + 2, column=2, padx=10, pady=10)

        

    # def first_button_action(self):
    #     self.column = 0
    #     self.row = 0
    #     for i, value in enumerate(self.widgets):
    #         self.widgets["notification_" + str(i)].grid_remove()
    #         self.notifications_to_send = []
    #     self.read_file()


    # def second_button_action(self):
    #     webbrowser.open("https://web.whatsapp.com")

    # def third_button_action(self):
    #     self.send_notifications()


    # def read_file(self):
    #     file_path = path.join("data", "meetings.log")
    #     if (path.exists(file_path) == True):
    #         with open(file_path, 'r') as file:
    #             filling_activated = False
    #             current_week = ""
    #             for line in file:
    #                 if line == "-------------------------------\n":
    #                     pass
    #                 elif filling_activated == True:
    #                     if line == "Notificated: True\n":
    #                         filling_activated = False
    #                     elif line == "Notificated: False\n":
    #                         pass
    #                     else: 
    #                         self.create_notifications(line)
    #                 elif line == "Notificated: False\n":
    #                         filling_activated = True
    #             self.school_counter = 0


    # def create_notifications(self, line):
    #     if line[:6] == "Semana":
    #         self.current_week = line
    #     else:
    #         assignation = ""
    #         name = ""
    #         companion = ""
    #         line = line.replace("\n", "")
    #         parts = line.split(": ")
    #         assignation = parts[0]
    #         name_part = parts[1]

    #         self.widgets["notification_" + str(self.loaded_notification)] = ctk.CTkCheckBox(master=self.frame, text=line, width=600, height=20, fg_color="#555555")
    #         self.widgets["notification_" + str(self.loaded_notification)].grid(row=self.row, column=self.column, padx=10, pady=10)
    #         self.row += 1
    #         self.loaded_notification += 1

    #         if assignation in ["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias", "Discurso estudiantil", "Análisis con el auditorio"]:
    #             self.school_counter += 1
    #             name_part = name_part.split(" - ")
    #             name = name_part[0]
    #             companion = name_part[1]
    #             self.notifications_to_send.append({"assignation": assignation, "name": name, "companion": companion, "current_week": self.current_week})
    #         else:
    #             name = name_part
    #             self.notifications_to_send.append({"assignation": assignation, "name": name, "current_week": self.current_week})


    # def send_notifications(self):
    #     print(self.notifications_to_send)


    # def set_notified(self):
    #     modified_once = False
    #     file_path = path.join("data", "meetings.log")
    #     if (path.exists(file_path) == True):
    #         with open(file_path, 'r') as file:
    #             lines = file.readlines()
    #         with open(file_path, 'w') as file:
    #             for line in lines:
    #                 if modified_once == False and line == "Notificated: False\n":
    #                         file.write("Notificated: True\n")
    #                         modified_once = True
    #                 else:
    #                     file.write(line)