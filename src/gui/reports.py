import customtkinter as ctk
import tkinter.filedialog as filedialog
import pyperclip
from src.database import DataBase


class ReportsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.db = DataBase()

        self.option_week = ctk.CTkOptionMenu(master=master, values=["Elegir semana"], width=430, height=36, command=self.load_report)
        self.button_copy = ctk.CTkButton(master=master, text="Copiar Reporte", width=190, height=36, command=self.copy_report)
        self.button_export = ctk.CTkButton(master=master, text="Exportar TXT", width=190, height=36, command=self.export_report)
        self.text_report = ctk.CTkTextbox(master=master, width=840, height=560)
        self.label_status = ctk.CTkLabel(master=master, text="", width=860, anchor="w")

        self.option_week.grid(row=0, column=0, padx=8, pady=(12, 8))
        self.button_copy.grid(row=0, column=1, padx=8, pady=(12, 8))
        self.button_export.grid(row=0, column=2, padx=8, pady=(12, 8))
        self.text_report.grid(row=1, column=0, padx=8, pady=8, columnspan=3)
        self.label_status.grid(row=2, column=0, padx=8, pady=(0, 8), columnspan=3, sticky="w")

        self.load_weeks()

    def load_weeks(self):
        weeks = self.db.read_meeting_weeks()
        self.option_week.configure(values=weeks)
        if weeks:
            self.option_week.set("Elegir semana")

    def load_report(self, week):
        report = self.db.read_meeting_report(week)
        self.text_report.delete("1.0", "end")
        self.text_report.insert("1.0", report)
        self.label_status.configure(text="")

    def copy_report(self):
        report = self.text_report.get("1.0", "end").strip()
        if not report:
            return
        pyperclip.copy(report)
        self.label_status.configure(text="Reporte copiado al portapapeles.")

    def export_report(self):
        report = self.text_report.get("1.0", "end").strip()
        if not report:
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
            initialfile="reunion_vida_ministerio.txt",
        )
        if not file_path:
            return
        with open(file_path, "w") as file:
            file.write(report + "\n")
        self.label_status.configure(text=f"Reporte exportado: {file_path}")
