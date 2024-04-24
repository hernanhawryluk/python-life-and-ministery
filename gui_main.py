import customtkinter as ctk
from gui_meetings import MeetingsFrame
from gui_replacements import ReplacementsFrame
from gui_participants import ParticipantsFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Reuniones Vida y Ministerio Teocrático")
        self.geometry("950x866")

        self.tab_view = TabView(master=self, anchor="nw", command=self.change_tab)
        self.tab_view.grid(row=0, column=0, padx=20, pady=10, columnspan=4)
        
    def change_tab(self):
        if self.tab_view.get() == "Reuniones":
            self.geometry("950x866")
        elif self.tab_view.get() == "Remplazos":
            self.geometry("950x866")
        elif self.tab_view.get() == "Participantes":
            self.geometry("950x300")

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Reuniones")
        self.add("Remplazos")
        self.add("Participantes")

        self.meetings_frame = MeetingsFrame(master=self.tab("Reuniones"))
        self.replacements_frame = ReplacementsFrame(master=self.tab("Remplazos"))
        self.participants_frame = ParticipantsFrame(master=self.tab("Participantes"))




