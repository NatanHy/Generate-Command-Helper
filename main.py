from GUI.gui import App
from GUI.app_functions import AppFunctions

if __name__ == "__main__":    
    app = App()
    AppFunctions.app = app
    app.mainloop()