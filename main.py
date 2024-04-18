from gui_main import App
from database import DataBase

if __name__ == "__main__":
    db = DataBase()
    db.create_database()
    app = App()
    app.mainloop()
