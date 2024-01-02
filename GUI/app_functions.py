from command_creation.command_file_parser import CommandParser
from command_creation.command_generator import CommandGenerator
from GUI.input_field import VariableInputField
from tkinter import filedialog
from os import getcwd

class AppFunctions:
    app = None
    template = None
    replace_consts = True
    shorten_var_names = True

    @classmethod
    def toggle_replace_consts(cls):
        cls.replace_consts = cls.app.const_replace_var.get()
        cls.update()

    @classmethod
    def toggle_shorten_var_names(cls):
        cls.shorten_var_names = cls.app.shorten_var_names_var.get()
        cls.update()

    @classmethod
    def get_current_text(cls):
        return str(cls.app.editor_textbox.get("0.0", "end"))

    @classmethod
    def update(cls):
        current_text_lines = cls.get_current_text().split("\n")
        template = CommandParser.parse_lines(current_text_lines)

        cls.template = template

        cls.update_consts()

        command = CommandGenerator(template)

        if cls.replace_consts:
            command = command.replace_consts()
        if cls.shorten_var_names:
            command = command.shorten_var_names()
        
        command = command.generate()
        
        cls.app.output_textbox.delete("0.0", "end")
        cls.app.output_textbox.insert("0.0", command)

        if len(command) > 256:
            cls.app.output_textbox.insert("end", "\n")
            cls.app.output_textbox.tag_add("make_grey","1.256" ,f"1.{len(command)}")
            cls.app.output_textbox.tag_config("make_grey", foreground="grey")
            cls.app.output_textbox.tag_add("warning", f"1.{len(command)}", "end")
            cls.app.output_textbox.tag_config("warning", foreground="red")
            cls.app.output_textbox.insert("end", "WARNING! command is longer than 256 characters")

    @classmethod
    def init_consts(cls):
        consts = cls.template.info.constants

        d = {}

        for const in consts:
            label_text = const.name
            input_text = const.value
            
            d[const.name] = VariableInputField(cls.app.const_frame, label_text, input_text)

        cls.app.variable_fields = d

    @classmethod
    def update_consts(cls):
        if len(cls.app.variable_fields) == 0:
            cls.init_consts()
        else:
            for const_name, var_field in cls.app.variable_fields.items():
                value = var_field.get_value()
                cls.template.change_const(const_name, value)

    @classmethod
    def save_file(cls):
        file = filedialog.asksaveasfile(
            initialdir=getcwd(),
            defaultextension=".txt"
            )
        
        if file is not None:
            text = str(cls.app.editor_textbox.get("0.0", "end"))
            file.write(text)
            file.close()

    @classmethod
    def load_file(cls):
        file = filedialog.askopenfile()

        if file is not None:
            current_text = cls.get_current_text()

            if len(current_text.strip()) > 0:
                response = cls.app.save_file_prompt()

                if response == "Cancel":
                    return
                elif response == "No":
                    pass
                elif response == "Yes":
                    cls.save_file()

            cls.app.editor_textbox.delete("0.0", "end")
            for line in file.readlines():
                cls.app.editor_textbox.insert("end", line)