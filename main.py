from gui import App
from database import DataBase

if __name__ == "__main__":
    db = DataBase("witnesses.db")
    app = App()
    app.mainloop()
