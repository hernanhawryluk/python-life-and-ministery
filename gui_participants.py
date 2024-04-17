import customtkinter as ctk

class ParticipantsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.entry_name = ctk.CTkEntry(master=master, placeholder_text="Nombre y apellido", width=205, height=40)
        self.entry_phone = ctk.CTkEntry(master=master, placeholder_text="Numbero de telefono", width=205, height=40)
        self.option_gender = ctk.CTkOptionMenu(master=master, values=["Hombre", "Mujer"], width=205, height=40)
        self.option_role = ctk.CTkOptionMenu(master=master, values=["Estudiante", "Estudiante +", "Ministerial", "Anciano"], width=200, height=40)
        self.checkbox_absence = ctk.CTkCheckBox(master=master, text="Ausente", font=("Arial", 14), width=205)
        self.checkbox_censored = ctk.CTkCheckBox(master=master, text="Censurado", font=("Arial", 14), width=205)
        self.checkbox_companion_only = ctk.CTkCheckBox(master=master, text="Solo acompañante", font=("Arial", 14), width=205)
        self.checkbox_allow_replacement = ctk.CTkCheckBox(master=master, text="Acepta remplazos", font=("Arial", 14), width=205)
        self.button_clear = ctk.CTkButton(master=master, text="Limpiar Datos", width=430, height=40, command=self.clear_data)
        self.button_save = ctk.CTkButton(master=master, text="Guardar Cambios", width=430,height=40)
        self.option_modify = ctk.CTkOptionMenu(master=master, values=["Hermano 1", "Hermano 2", "Hermano 3"], width=430, height=40)
        self.button_modify = ctk.CTkButton(master=master, text="Modificar Participante", width=205, height=40)
        self.button_delete = ctk.CTkButton(master=master, text="Borrar Participante", width=205,height=40)
        self.entry_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_phone.grid(row=0, column=1, padx=10, pady=10)
        self.option_gender.grid(row=0, column=2, padx=10, pady=10)
        self.option_role.grid(row=0, column=3, padx=10, pady=10)
        self.checkbox_absence.grid(row=1, column=0, padx=10, pady=10)
        self.checkbox_censored.grid(row=1, column=1, padx=10, pady=10)
        self.checkbox_companion_only.grid(row=1, column=2, padx=10, pady=10)
        self.checkbox_allow_replacement.grid(row=1, column=3, padx=10, pady=10)
        self.button_clear.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.button_save.grid(row=2, column=2, padx=10, pady=10, columnspan=2)
        self.option_modify.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        self.button_modify.grid(row=3, column=2, padx=10, pady=10)
        self.button_delete.grid(row=3, column=3, padx=10, pady=10)

    def save_data(self):
        self.entry_name.get()
        self.entry_phone.get()
        self.option_gender.get()
        self.option_role.get()
        self.checkbox_absence.get()
        self.checkbox_censored.get()
        self.checkbox_companion_only.get()
        self.checkbox_allow_replacement.get()

    def clear_data(self):
        self.entry_name.delete(0, "end")
        self.entry_phone.delete(0, "end")
        self.option_gender.set("Hombre")
        self.option_role.set("Estudiante")
        self.checkbox_absence.deselect()
        self.checkbox_censored.deselect()
        self.checkbox_companion_only.deselect()
        self.checkbox_allow_replacement.deselect()

    def modify_data(self):
        pass

    def delete_data(self):
        pass