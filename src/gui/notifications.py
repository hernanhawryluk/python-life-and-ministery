import customtkinter as ctk
from src.database import DataBase
from src.utils.switchers import meeting_switcher
from os import path
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NotificationsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets = {}
        self.select_week = ""
        self.school_counter = 0
        self.db = DataBase()
        
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
        
        self.button_lead_weeks = ctk.CTkButton(master=master, text="Cargar semanas", font=("Arial", 16), width=300, height=36, command=self.on_click_load_weeks)
        self.option_week_selector = ctk.CTkOptionMenu(master=master, width=268, height=36, anchor="center", command=self.on_click_select_week)
        self.button_open_whatsapp = ctk.CTkButton(master=master, text="Envío Automatizado", font=("Arial", 16), width=268, height=36, command=self.on_click_automatized)
        self.option_week_selector.set("← Cargar semanas")

        self.button_lead_weeks.grid(row=0, column=0, padx=10, pady=(20, 10), columnspan=2)
        self.option_week_selector.grid(row=0, column=2, padx=10, pady=(20, 10))
        self.button_open_whatsapp.grid(row=0, column=3, padx=10, pady=(20, 10))

        self.label_copy = ctk.CTkLabel(master=master, text=" ▼  Copia al portapapeles", font=("Arial", 18), width=305, anchor="w")
        self.label_copy.grid(row=1, column=0, padx=10, pady=(6, 10), columnspan=2)

        for i, value in enumerate(self.assignations):
            if (value["school"] == True):
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text="", font=("Arial", 16), width=0, state=value["state"], text_color_disabled="#FFFFFF", command=lambda key=self.assignations[i]["key"]: self.on_click_school_checkbox(key))
                self.widgets["option_type_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Explique sus creencias" , "Discurso estudiantil", "Análisis con el auditorio"], width=250)
                self.widgets["option_type_" + self.assignations[i]["key"]].set(value["text"])
                self.widgets["option0_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=268)
                self.widgets["option1_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=268)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i + 2, column=0, padx=10, pady=10)
                self.widgets["option_type_" + self.assignations[i]["key"]].grid(row=i + 2, column=1, padx=10, pady=10, sticky="nsew")
                self.widgets["option0_" + self.assignations[i]["key"]].grid(row=i + 2, column=2, padx=10, pady=10)
                self.widgets["option1_" + self.assignations[i]["key"]].grid(row=i + 2, column=3, padx=10, pady=10)

            else:
                self.widgets["checkbox_" + self.assignations[i]["key"]] = ctk.CTkCheckBox(master=master, text=value["text"], font=("Arial", 16), state=value["state"], width=300, text_color_disabled="#FFFFFF", command=lambda key=self.assignations[i]["key"]: self.on_click_checkbox(key))
                self.widgets["option_" + self.assignations[i]["key"]] = ctk.CTkOptionMenu(master=master, values=[""], width=268)

                self.widgets["checkbox_" + self.assignations[i]["key"]].grid(row=i + 2, column=0, columnspan=2, padx=10, pady=10)
                self.widgets["option_" + self.assignations[i]["key"]].grid(row=i + 2, column=2, padx=10, pady=10)

        
    def on_click_load_weeks(self):
        file_path = path.join("data", "meetings.log")
        if (path.exists(file_path) == True):
            file = open(file_path, 'r')
            weeks_options = []
            for line in file:
                if line[:6] == "Semana":
                    weeks_options.append(line.replace("\n", ""))
            self.option_week_selector.configure(values=weeks_options)


    def on_click_select_week(self, key):
        self.selected_week = key
        self.load_week()


    def on_click_automatized(self):
        week = self.selected_week
        messages = []

        for i, value in enumerate(self.assignations):
            checkbox_ref = "checkbox_" + self.assignations[i]["key"]
            if (value["school"] == True):
                assignment = self.widgets["option_type_" + self.assignations[i]["key"]].get()
                titular = self.widgets["option0_" + self.assignations[i]["key"]].get()
                companion = self.widgets["option1_" + self.assignations[i]["key"]].get()
                message = "Asignación para la reunión vida y ministerio teocrático:\n\n" + week + "\n" + "Asignación: " + assignment + ".\n" + "Titular: " + titular + ".\n" + "Ayudante: " + companion + "."
            else:
                assignment = self.widgets["checkbox_" + self.assignations[i]["key"]].cget("text")
                titular = self.widgets["option_" + self.assignations[i]["key"]].get()
                message = "Asignación para la reunión vida y ministerio teocrático:\n\n" + week + "\n" + "Asignación: " + assignment + ".\n" + "Titular: " + titular + "."
            phone_number = self.db.get_phone_number(titular)
            if phone_number != None and phone_number != "":
                messages.append({"phone_number": phone_number, "message": message, "checkbox_ref": checkbox_ref})
        
        print(messages)
        # self.send_atomatized_notifications(messages)

                
    def send_atomatized_notifications(self, messages):
        driver = webdriver.Chrome()
        base_url = 'https://web.whatsapp.com'
        driver.get(base_url)
        time.sleep(30)
        for message in messages:
            same_tab = (base_url + "/send?phone=+" + str(message["phone_number"]) + "&text=" + str(message["message"]))
            driver.get(same_tab)
            time.sleep(5)
            content = driver.switch_to.active_element
            content.send_keys(Keys.RETURN)
            time.sleep(2)
            self.widgets[message["checkbox_ref"]].select()


    def on_click_school_checkbox(self, key):
        week = self.selected_week
        assignment = self.widgets["option_type_" + key].get()
        name = self.widgets["option0_" + key].get()
        companion = self.widgets["option1_" + key].get()

        message = "Asignación para la reunión vida y ministerio teocrático:\n\n" + week + "\n" + "Asignación: " + assignment + ".\n" + "Titular: " + name + ".\n" + "Ayudante: " + companion + "."
        pyperclip.copy(message)

    
    def on_click_checkbox(self, key):
        week = self.selected_week
        assignment = self.widgets["checkbox_" + key].cget("text")
        name = self.widgets["option_" + key].get()

        message = "Asignación para la reunión vida y ministerio teocrático:\n\n" + week + "\n" + "Asignación: " + assignment + ".\n" + "Titular: " + name + "."
        pyperclip.copy(message)


    def load_week(self):
        file_path = path.join("data", "meetings.log")
        if (path.exists(file_path) == True):
            file = open(file_path, 'r')
            filling_activated = False
            for line in file:
                if line[:6] == "Semana":
                    if line.replace("\n", "") == self.selected_week:
                        filling_activated = True
                elif filling_activated == True:
                    if line == "-------------------------------\n":
                        break
                    else:
                        self.fill_assignation(line.replace("\n", ""))
            self.school_counter = 0

    
    def fill_assignation(self, line):
        assignment_and_name = line.split(": ")
        assignment = assignment_and_name[0]
        name_or_names = assignment_and_name[1]
        if " - " in name_or_names:
            self.school_counter += 1
            name_or_names = name_or_names.split(" - ")
            name = name_or_names[0]
            companion = name_or_names[1]
            self.widgets["option_type_school_" + str(self.school_counter)].set(assignment)
            self.widgets["option0_school_" + str(self.school_counter)].set(name)
            self.widgets["option1_school_" + str(self.school_counter)].set(companion)
        else:
            name = name_or_names
            short_assignment = meeting_switcher(assignment)
            self.widgets["option_" + short_assignment].set(name)
