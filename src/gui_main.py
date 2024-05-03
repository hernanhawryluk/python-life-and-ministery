import customtkinter as ctk
from src.gui.meetings import MeetingsFrame
from src.gui.replacements import ReplacementsFrame
from src.gui.participants import ParticipantsFrame
from src.gui.notifications import NotificationsFrame
from src.gui.clean import CleanFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Reuniones Vida y Ministerio Teocrático")
        self.geometry("956x870")

        self.tab_view = TabView(master=self, anchor="nw", command=self.change_tab)
        self.tab_view.grid(row=0, column=0, padx=20, pady=10, columnspan=4)
        
    def change_tab(self):
        if self.tab_view.get() == "Reuniones":
            self.geometry("956x870")
        elif self.tab_view.get() == "Remplazos":
            self.geometry("956x870")
        elif self.tab_view.get() == "Participantes":
            self.geometry("950x300")
        elif self.tab_view.get() == "Notificaciones":
            self.geometry("956x910")
        elif self.tab_view.get() == "Limpiar":
            self.geometry("956x910")

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Reuniones")
        self.add("Remplazos")
        self.add("Participantes")
        self.add("Notificaciones")
        self.add("Limpiar")

        self.meetings_frame = MeetingsFrame(master=self.tab("Reuniones"))
        self.replacements_frame = ReplacementsFrame(master=self.tab("Remplazos"))
        self.participants_frame = ParticipantsFrame(master=self.tab("Participantes"))
        self.configurations_frame = NotificationsFrame(master=self.tab("Notificaciones"))
        self.clean_frame = CleanFrame(master=self.tab("Limpiar"))




