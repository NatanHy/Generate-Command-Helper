import tkinter
from CTkMessagebox import CTkMessagebox
import customtkinter
from GUI.app_functions import AppFunctions
from GUI.fonts import MONOSPACE

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Generate Command Helper")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Command Helper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.generator_button = customtkinter.CTkButton(self.sidebar_frame, text="Generator", command=self.toggle_generator_event)
        self.generator_button.grid(row=1, column=0, padx=20, pady=10)
        self.editor_button = customtkinter.CTkButton(self.sidebar_frame, text="Editor", command=self.toggle_editor_event)
        self.editor_button.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.generator_window()
        self.editor_window()
        self.toggle_generator_event()

        # set default values
        self.const_replace_checkbox.select()
        self.short_var_checkbox.select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def generator_window(self):
        # create main button
        self.generate_button = customtkinter.CTkButton(
            text="Generate", 
            command=AppFunctions.update, 
            master=self, 
            border_width=2, 
            font=("CTkDefaultFont", 30, "bold")
            )

        # create textbox
        self.output_textbox = customtkinter.CTkTextbox(self, width=250, font=MONOSPACE)

        # create scrollable frames
        self.const_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")

        self.variable_fields = {}

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.scrollable_frame_labels_1 = []

        self.const_replace_var = tkinter.BooleanVar(value=True)
        self.const_replace_checkbox = customtkinter.CTkCheckBox(
            text="Replace constant values",
            master=self.checkbox_slider_frame, 
            command=AppFunctions.toggle_replace_consts, 
            variable=self.const_replace_var
            )

        self.shorten_var_names_var = tkinter.BooleanVar(value=True)
        self.short_var_checkbox = customtkinter.CTkCheckBox(
            text="Shorten variable names",
            master=self.checkbox_slider_frame,
            command=AppFunctions.toggle_shorten_var_names,
            variable=self.shorten_var_names_var
            )
        
        self.generator_elements = [
            self.generate_button,
            self.output_textbox,
            self.const_frame,
            self.checkbox_slider_frame,
            self.const_replace_checkbox,
            self.short_var_checkbox,
        ]

    def editor_window(self):
        # create textbox
        self.editor_textbox = customtkinter.CTkTextbox(self, font=MONOSPACE)

        #Save button
        self.save_button = customtkinter.CTkButton(
            text="Save", 
            command=AppFunctions.save_file, 
            master=self, fg_color="transparent", 
            border_width=2, 
            text_color=("gray10", "#DCE4EE"),
            font=("CTkDefaultFont", 10, "bold")
            )        
        
        #Load button
        self.load_button = customtkinter.CTkButton(
            text="Load file", 
            command=AppFunctions.load_file, 
            master=self, fg_color="transparent", 
            border_width=2, 
            text_color=("gray10", "#DCE4EE"),
            font=("CTkDefaultFont", 10, "bold")
            )    

        self.editor_elements = [
            self.editor_textbox,
            self.save_button,
            self.load_button
        ]

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def toggle_generator_event(self):
        for elm in self.editor_elements:
            elm.grid_forget()
    
        self.generate_button.grid(row=3, column=3, padx=20, pady=(0, 20), sticky="nsew")
        self.output_textbox.grid(row=3, column=1, padx=(20, 0), pady=(0, 20), sticky="nsew")
        self.const_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.const_replace_checkbox.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.short_var_checkbox.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")

    def save_file_prompt(self):
        msgbox = CTkMessagebox(
            message="Save current file before loading?", 
            option_1="Cancel",
            option_2="No",
            option_3="Yes"
            )
        
        return msgbox.get()

    def toggle_editor_event(self):
        for elm in self.generator_elements:
            elm.grid_forget()

        self.editor_textbox.grid(row=0, column=1, padx=10, pady=10, columnspan=3, rowspan=3, sticky="nsew")
        self.save_button.grid(row=3, column=3, padx=(0, 10), pady=(0, 10), sticky="se")
        self.load_button.grid(row=3, column=2, padx=(0, 10), pady=(0, 10), sticky="se")
