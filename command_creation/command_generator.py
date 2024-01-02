from command_creation.command_template import CommandTemplate
from command_creation.command_tokens import *
from string import ascii_letters

RESERVED_VAR_NAMES = ["x", "y", "z", "type", "data"]
POSSIBLE_VAR_NAMES = [letter for letter in ascii_letters if letter not in RESERVED_VAR_NAMES]

class CommandGenerator:
    def __init__(self, template : CommandTemplate):
        self.template = template

        self._const_replace = False
        self._short_var = False

        self._const_values = {}
        self._var_mapping = {}

    def replace_consts(self):
        self._const_replace = True

        self._const_values = {c.name:c.value for c in self.template.info.constants}

        return self
    
    def shorten_var_names(self):
        self._short_var = True

        variables = self.template.info.variables
        variable_names = [v.name for v in variables]

        valid_var_names = [
            l for l in POSSIBLE_VAR_NAMES if not l in self._const_values and l not in variable_names
            ]

        num_of_replaced_vars = 0

        for var in variables:
            if len(var.name) > 1:
                if var.name not in self._var_mapping:
                    self._var_mapping[var.name] = valid_var_names[num_of_replaced_vars]
                    num_of_replaced_vars += 1
            else:
                self._var_mapping[var.name] = var.name

        return self

    def generate(self):
        s = ""

        skip = False

        for token in self.template.tokens:
            if skip:
                skip = False
                continue

            replaced_string = False

            if self._const_replace:
                if isinstance(token, CommandConstToken):
                    replaced_string = True
                    if token.declaration:
                        skip = True
                    else:
                        s += token.const.value

            if self._short_var:
                if isinstance(token, CommandVarToken):
                    replaced_string = True
                    s += self._var_mapping[token.var.name]

            if not replaced_string:
                s += token.get_string()
                replaced_string = False

        return s