import customtkinter as ctk
from src.database import DataBase
from src.utils.switchers import meeting_switcher, determiner_switcher
from os import path
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class NotificationsFrame(ctk.CTkFrame):
    def __init__(self, master, tabview):
        super().__init__(master)
        self.widgets = {}
        self.select_week = ""
        self.school_counter = 0
        self.db = DataBase()
        self.dialog_window = None
        self.driver = None
        self.tabview = tabview
        
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
        
        self.option_week_selector = ctk.CTkOptionMenu(master=master,  values=["Elegir semana"], width=590, height=34, anchor="center", command=self.on_click_select_week)
        self.button_send_assignments = ctk.CTkButton(master=master, text="Conectar WhatsApp",font=("Arial", 16), width=268, height=34, command=self.on_click_automatized)
        
        self.option_week_selector.grid(row=0, column=0, padx=10, pady=(20, 10), columnspan=3)
        self.button_send_assignments.grid(row=0, column=3, padx=10, pady=(20, 10))
        
        self.label_copy = ctk.CTkLabel(master=master, text=" ▼  Copia al portapapeles", font=("Arial", 18), width=305, anchor="w")
        self.label_copy.grid(row=1, column=0, padx=10, pady=(4, 2), columnspan=2)
        self.checkbox_only_reminders = ctk.CTkCheckBox(master=master, text="Solo recordatorios",font=("Arial", 16), width=170, height=36)
        self.checkbox_only_reminders.grid(row=1, column=3, padx=10, pady=(4, 2))

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


    def open_dialog_window(self):
        if self.dialog_window is None or not self.dialog_window.winfo_exists():
            self.dialog_window = ToplevelWindow(self)
        else:
            self.dialog_window.focus()
    

    def load_weeks(self):
        file_path = path.join("data", "meetings.log")
        if (path.exists(file_path) == True):
            file = open(file_path, 'r')
            weeks_options = []
            for line in file:
                if line[:6] == "Semana":
                    weeks_options.append(line.replace("\n", ""))
            self.option_week_selector.configure(values=weeks_options)
            if len(weeks_options) > 0:
                self.option_week_selector.set("Elegir semana")


    def on_click_select_week(self, key):
        for i, value in enumerate(self.assignations):
                self.widgets["checkbox_" + self.assignations[i]["key"]].deselect()
        self.selected_week = key
        self.load_week()
        if self.driver != None:
            self.button_send_assignments.configure(text="Envío Automatizado")


    def on_click_automatized(self):
        if self.driver == None:
            try:
                self.driver = webdriver.Chrome()
                base_url = 'https://web.whatsapp.com'
                self.driver.get(base_url)
                if self.option_week_selector.get() != "Elegir semana":
                    self.button_send_assignments.configure(text="Envío Automatizado")
                else:
                    self.button_send_assignments.configure(text="Desconectar WhatsApp")
            except Exception as e:
                print(e)

        elif self.driver != None and self.button_send_assignments.cget("text") == "Desconectar WhatsApp":
            try:
                self.driver.quit()
                self.driver = None
                self.button_send_assignments.configure(text="Conectar WhatsApp")
            except Exception as e:
                print(e)

        else:
            if self.option_week_selector.get() != "Elegir semana":
                week = self.selected_week
                messages = []

                for i, value in enumerate(self.assignations):
                    checkbox_ref = "checkbox_" + self.assignations[i]["key"]
                    if (value["school"] == True):
                        assignment = self.widgets["option_type_" + self.assignations[i]["key"]].get()
                        titular = self.widgets["option0_" + self.assignations[i]["key"]].get()
                        companion = self.widgets["option1_" + self.assignations[i]["key"]].get()
                        if self.checkbox_only_reminders.get() == 0:
                            message = [f"¡Hola {titular.split(' ')[0]}! Espero que te encuentres bien. Te envío tu asignación para la reunión Vida y Ministerio Cristianos:", "", str(week), "Asignación: " + assignment, "Titular: " + titular, "Ayudante: " + companion]
                        else:
                            message = [self.reminder_message_generator(titular, assignment)]
                    else:
                        assignment = self.widgets["checkbox_" + self.assignations[i]["key"]].cget("text")
                        titular = self.widgets["option_" + self.assignations[i]["key"]].get()
                        if self.checkbox_only_reminders.get() == 0:
                            message = [f"¡Hola {titular.split(' ')[0]}! Espero que te encuentres bien. Te envío tu asignación para la reunión Vida y Ministerio Cristianos:", "", str(week), "Asignación: " + assignment, "Titular: " + titular]
                        else:
                            message = [self.reminder_message_generator(titular, assignment)]
                    phone_number = self.db.get_phone_number(titular)
                    if phone_number != None and phone_number != "":
                        messages.append({"phone_number": phone_number, "message": message, "checkbox_ref": checkbox_ref})
                self.send_atomatized_notifications(messages)


    def reminder_message_generator(self, titular, assignment):
        name_and_surname = titular.split(" ")
        only_name = name_and_surname[0]
        assignment_with_determiner = determiner_switcher(assignment)
        message = "Hola " + only_name + "! Te escribo a modo de recordatorio. En la reunión de esta semana tenés " + assignment_with_determiner + ". Nos vemos allá. ¡Saludos!"
        return message


    def send_atomatized_notifications(self, messages):
        try:
            for message in messages:
                search_box = WebDriverWait(self.driver, 60).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "selectable-text")))
                search_box[0].click()
                time.sleep(1)
                search_box[0].send_keys(message["phone_number"])
                time.sleep(1)
                search_box[0].send_keys(Keys.RETURN)
                time.sleep(2)
                input_box = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')))
                input_box.click()
                time.sleep(1)
                for line in message["message"]:
                    input_box.send_keys(line)
                    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
                time.sleep(1)
                input_box.send_keys(Keys.ENTER)
                time.sleep(2)
                self.widgets[message["checkbox_ref"]].select()

            self.button_send_assignments.configure(text="Desconectar WhatsApp")
        except Exception as e:
            print(e)


    def on_click_school_checkbox(self, key):
        if self.option_week_selector.get() != "Elegir semana":
            week = self.selected_week
            assignment = self.widgets["option_type_" + key].get()
            name = self.widgets["option0_" + key].get()
            companion = self.widgets["option1_" + key].get()
            message = ""
            if self.checkbox_only_reminders.get() == 0:
                message = "Asignación para la reunión vida y ministerio teocrático:\n\n" + week + "\n" + "Asignación: " + assignment + ".\n" + "Titular: " + name + ".\n" + "Ayudante: " + companion + "."
            else:
                message = self.reminder_message_generator(name, assignment)
            pyperclip.copy(message)
            self.open_dialog_window()

    
    def on_click_checkbox(self, key):
        if self.option_week_selector.get() != "Elegir semana":
            week = self.selected_week
            assignment = self.widgets["checkbox_" + key].cget("text")
            name = self.widgets["option_" + key].get()
            message = ""
            if self.checkbox_only_reminders.get() == 0:
                message = "Asignación para la reunión vida y ministerio teocrático:\n\n" + week + "\n" + "Asignación: " + assignment + ".\n" + "Titular: " + name + "."
            else:
                message = self.reminder_message_generator(name, assignment)
            pyperclip.copy(message)
            self.open_dialog_window()


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
            file.close()

    
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


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        window_width = 400
        window_height = 70
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.title("Mensaje copiado")
        self.label = ctk.CTkLabel(self, text="El mensaje se ha copiado al portapapeles.", font=("Arial", 18))
        self.label.pack(padx=20, pady=20)

        self.after(2000, self.destroy)
        