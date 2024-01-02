import customtkinter
import tkinter
from GUI.fonts import MONOSPACE

class VariableInputField:
    def __init__(self, master, variable_name, initial_value):
        from GUI.app_functions import AppFunctions

        self.variable_name = variable_name

        # Label displaying the variable name (read-only)
        self.label = customtkinter.CTkLabel(master, text=f"{variable_name} :", font=MONOSPACE)
        self.label.grid(sticky="w")  # Align label to the right

        # Entry field for the variable value
        self.entry_var = customtkinter.StringVar(value=initial_value)
        self.entry = customtkinter.CTkEntry(
            master, 
            textvariable=self.entry_var, 
            font=MONOSPACE, 
            width=300,
            )
        self.entry.grid(sticky="w", row=len(master.winfo_children())+1, column=0)
        self.entry.bind("<<Modified>>", AppFunctions.update_consts)

        self.entry_var.trace_add("write", lambda *args: AppFunctions.update())

    def get_value(self):
        return self.entry_var.get()