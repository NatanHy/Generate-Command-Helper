from command_creation.command_template import CommandTemplate
from command_creation.command_tokens import CommandVariable, CommandConstant

ALLOWED_VAR_SYMBOLS = ["_", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
EXPRESSION_END_SYMBOLS = [";", "}"]

class CommandParser:
    @staticmethod
    def parse_lines(lines) -> CommandTemplate:
        command_template = CommandTemplate()

        first_line = True
        current_token = ""
        const_name = ""
        token_is_const = True
        look_for_const_value = False

        constants = {}
        var_names = []

        for line in lines:
            if first_line:
                command_template.set_command(line.strip() + " ")
                first_line = False
                continue
            
            for ch in line.strip().replace(" ", ""):
                #If looking for value of const, only stop at expression ending symbols (ex. ;)
                if look_for_const_value:
                    if ch in EXPRESSION_END_SYMBOLS:
                        const = CommandConstant(const_name, current_token)
                        constants[const_name] = const

                        command_template.add_const(const)
                        command_template.add_str(ch)


                        look_for_const_value = False
                        current_token = ""
                    else:
                        current_token += ch
                #Else stop at all non-variable symbols
                elif not is_var_str(ch):
                    if ch == "=": #Variable is being assigned
                        if len(current_token) == 0:
                            #Case where previous character is special (ex. +=)
                            command_template.add_str(ch)
                            continue

                        if token_is_const:
                            const_name = current_token
                            look_for_const_value = True
                        else:
                            command_template.add_var(CommandVariable(current_token))
                            var_names.append(current_token)
                            command_template.add_str(ch)
                    else:
                        #Also add usages of constants as const token
                        if current_token in constants:
                            command_template.add_const(constants[current_token])
                        elif current_token in var_names:
                            command_template.add_var(CommandVariable(current_token))
                        else:
                            command_template.add_str(current_token)
                        command_template.add_str(ch)
                    #Reset current token
                    current_token = ""
                else:
                    current_token += ch

                is_uppercase = is_var_str(ch, only_upper=True)
                only_one_upper = len(current_token) == 1 and is_uppercase
                token_is_const = only_one_upper or (token_is_const and is_uppercase)

        return command_template        

    @staticmethod
    def parse_file(file_path : str) -> CommandTemplate:
        try:
            with open(file_path, "r") as f:
                return CommandParser.parse_lines(f.readlines())
        except Exception as e:
            print(e)
            return None
    
def is_var_str(s, only_upper=False):
    for c in s:
        if not (c.isalnum() or c in ALLOWED_VAR_SYMBOLS):
            return False
        if only_upper and not (c.isupper() or c in ALLOWED_VAR_SYMBOLS):
            return False
    return True