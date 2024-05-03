import customtkinter as ctk
from src.database import DataBase

class CleanFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.db = DataBase()
        self.button_clean_db = ctk.CTkButton(master=master, text="Limpiar Base de Datos", width=430, height=40, command=self.clean_db)
        self.button_clean_db.grid(row=0, column=0, padx=10, pady=10)
        

    def clean_db(self):
        self.db.clean()
