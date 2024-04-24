import customtkinter as ctk
from src.database import DataBase

class ParticipantsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.db = DataBase()
        self.to_modify = None
        self.all_data = self.db.read_all_names()
        self.all_witnesses = [f"{data[0]}" for data in self.all_data]
        
        self.entry_name = ctk.CTkEntry(master=master, placeholder_text="Nombre y apellido", width=205, height=40)
        self.entry_phone = ctk.CTkEntry(master=master, placeholder_text="Numbero de telefono", width=205, height=40)
        self.option_gender = ctk.CTkOptionMenu(master=master, values=["Hombre", "Mujer"], width=205, height=40)
        self.option_role = ctk.CTkOptionMenu(master=master, values=["Estudiante", "Estudiante +", "Ministerial", "Anciano"], width=200, height=40)
        self.checkbox_exclude = ctk.CTkCheckBox(master=master, text="Omitir temporalmente", font=("Arial", 14), width=205)
        self.checkbox_custom = ctk.CTkCheckBox(master=master, text="Limitado por edad", font=("Arial", 14), width=205)
        self.checkbox_companion_only = ctk.CTkCheckBox(master=master, text="Solo acompañante", font=("Arial", 14), width=205)
        self.checkbox_allow_replacement = ctk.CTkCheckBox(master=master, text="Acepta remplazos", font=("Arial", 14), width=205)
        self.button_clear = ctk.CTkButton(master=master, text="Limpiar Datos", width=430, height=40, command=self.clear_data)
        self.button_save = ctk.CTkButton(master=master, text="Guardar Cambios", width=430,height=40, command=self.save_data)
        self.option_modify = ctk.CTkOptionMenu(master=master, values=self.all_witnesses, width=430, height=40)
        if self.all_witnesses == []: 
            self.option_modify.set("Participantes")
        self.button_modify = ctk.CTkButton(master=master, text="Modificar Participante", width=205, height=40, command=self.modify_data)
        self.button_delete = ctk.CTkButton(master=master, text="Borrar Participante", width=205, height=40, command=self.delete_data)

        self.entry_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_phone.grid(row=0, column=1, padx=10, pady=10)
        self.option_gender.grid(row=0, column=2, padx=10, pady=10)
        self.option_role.grid(row=0, column=3, padx=10, pady=10)
        self.checkbox_exclude.grid(row=1, column=0, padx=10, pady=10)
        self.checkbox_custom.grid(row=1, column=1, padx=10, pady=10)
        self.checkbox_companion_only.grid(row=1, column=2, padx=10, pady=10)
        self.checkbox_allow_replacement.grid(row=1, column=3, padx=10, pady=10)
        self.button_clear.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.button_save.grid(row=2, column=2, padx=10, pady=10, columnspan=2)
        self.option_modify.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        self.button_modify.grid(row=3, column=2, padx=10, pady=10)
        self.button_delete.grid(row=3, column=3, padx=10, pady=10)

    def save_data(self):
        values = [
            self.entry_name.get(),
            self.entry_phone.get(),
            self.option_gender.get(),
            self.option_role.get(),
            self.checkbox_exclude.get(),
            self.checkbox_custom.get(),
            self.checkbox_companion_only.get(),
            self.checkbox_allow_replacement.get()
        ]
        if (values[0] == ""):
            print("Name is required")
            return

        if self.to_modify is None:
            self.db.create_new(values)
        else:
            self.db.modify_one(self.to_modify, values)
            self.to_modify = None

        self.all_witnesses.append(values[0])
        self.option_modify.configure(values=self.all_witnesses)
        self.option_modify.set(values[0])
        self.clear_data()
        

    def clear_data(self):
        self.entry_name.delete(0, "end")
        self.entry_phone.delete(0, "end")
        self.checkbox_exclude.deselect()
        self.checkbox_custom.deselect()
        self.checkbox_companion_only.deselect()
        self.checkbox_allow_replacement.deselect()

    def modify_data(self):
        name = self.option_modify.get()
        witness = self.db.read_one(name)[0]
        self.clear_data()
        self.entry_name.insert(0, witness[1])
        self.entry_phone.insert(0, witness[2])
        self.option_gender.set(witness[3])
        self.option_role.set(witness[4])
        if witness[5] == 1: self.checkbox_exclude.select()
        if witness[6] == 1: self.checkbox_custom.select()
        if witness[7] == 1: self.checkbox_companion_only.select()
        if witness[8] == 1: self.checkbox_allow_replacement.select()
        self.all_witnesses.remove(name)
        self.to_modify = witness[0]

    def delete_data(self):
        name = self.option_modify.get()
        self.db.delete_one(name)
        self.all_witnesses.remove(name)
        if self.all_witnesses == []: 
            self.option_modify.set("Participantes")
        else:
            self.option_modify.configure(values=self.all_witnesses)
            self.option_modify.set(self.all_witnesses[0])

