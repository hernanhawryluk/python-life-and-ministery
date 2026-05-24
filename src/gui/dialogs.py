import customtkinter as ctk


class MessageDialog(ctk.CTkToplevel):
    def __init__(self, master, title, lines):
        super().__init__(master)

        self.title(title)
        self.geometry("520x260")
        self.resizable(False, False)

        text = "\n".join(lines)
        self.label = ctk.CTkLabel(self, text=text, font=("Arial", 15), justify="left", anchor="w")
        self.label.pack(padx=20, pady=(20, 12), fill="both", expand=True)

        self.button = ctk.CTkButton(self, text="Aceptar", width=120, command=self.destroy)
        self.button.pack(pady=(0, 18))
