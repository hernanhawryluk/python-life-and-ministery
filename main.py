from src.gui_main import App
from src.database import DataBase

if __name__ == "__main__":
    db = DataBase()
    db.create_database()
    app = App()
    app.mainloop()
