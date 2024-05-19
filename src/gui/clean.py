import customtkinter as ctk
from src.database import DataBase
from os import path

class CleanFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.db = DataBase()

        self.label_clear_logs = ctk.CTkLabel(master=master, text="Limpiar registros anteriores:", width=430, anchor="w", font=("Arial", 17))
        self.option_clear_logs = ctk.CTkOptionMenu(master=master, width=430, height=40)
        self.button_clear_logs = ctk.CTkButton(master=master, text="Limpiar Semana", width=430, height=40, command=self.clear_logs)
        self.label_clear_logs.grid(row=0, column=0, padx=10, pady=10)
        self.option_clear_logs.grid(row=1, column=0, padx=10, pady=10)
        self.button_clear_logs.grid(row=2, column=0, padx=10, pady=10)
        
        self.label_clean_db = ctk.CTkLabel(master=master, text="Limpiar base de datos:", width=430, anchor="w", font=("Arial", 17))
        self.button_clean_db = ctk.CTkButton(master=master, text="Limpiar Base de Datos", width=430, height=40, command=self.clean_db)
        self.label_clean_db.grid(row=3, column=0, padx=10, pady=10)
        self.button_clean_db.grid(row=4, column=0, padx=10, pady=10)

        self.load_weeks()


    def clean_db(self):
        self.db.clean()


    def clear_logs(self):
        content_to_save = ["-------------------------------\n"]
        delete_between = False
        to_keep = False
        erase_until = self.option_clear_logs.get()
        if erase_until != "Elegir hasta que registro se debe limpiar":
            file_path = path.join("data", "meetings.log")
            if (path.exists(file_path) == True):
                file = open(file_path, 'r')
                lines = file.readlines()
                for line in lines:
                    if line.replace("\n", "") == erase_until:
                        delete_between = True
                    elif delete_between == True and line == "-------------------------------\n" and to_keep == False:
                        to_keep = True
                    elif to_keep == True:
                        content_to_save.append(line)
                file.close()
                write_file = open(file_path, "w")
                write_file.writelines(content_to_save)        
                write_file.close()
                print("success!")
        self.load_weeks()
                

    def load_weeks(self):
        file_path = path.join("data", "meetings.log")
        if (path.exists(file_path) == True):
            file = open(file_path, 'r')
            weeks_options = []
            for line in file:
                if line[:6] == "Semana":
                    weeks_options.append(line.replace("\n", ""))
            self.option_clear_logs.configure(values=weeks_options)
            if len(weeks_options) > 0:
                self.option_clear_logs.set("Elegir hasta que registro se debe limpiar")
            file.close()
