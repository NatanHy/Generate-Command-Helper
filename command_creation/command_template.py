from command_creation.command_tokens import *


class CommandInfo:
    def __init__(self, d):
        self.d = d

    @property
    def command(self):
        return self.d["command"]
    
    @property
    def constants(self):
        return self.d["constants"]
    
    @property
    def variables(self):
        return self.d["variables"]

class CommandTemplate:
    def __init__(self):
        self.tokens = []

        self._command = ""
        self._consts = []
        self._variables = []

    @property
    def info(self):
        return CommandInfo({
            "command" : self._command,
            "constants" : [c.const for c in self._consts],
            "variables" : [v.var for v in self._variables]
        })
    
    def change_const(self, const_name : str, new_value : str):
        for c in self.info.constants:
            if c.name == const_name:
                c.value = new_value
                break

    def set_command(self, cmd : str):
        self._command = cmd
        self.tokens.append(CommandStringToken(cmd))

    def add_const(self, const : CommandConstant):
        token = CommandConstToken(const)

        for const_token in self._consts:
            if const_token == token:
                self.tokens.append(const_token.non_declared_shallow_copy())
                break
        else:
            self.tokens.append(token)
            self._consts.append(token)

    def add_var(self, var : CommandVariable):
        token = CommandVarToken(var)
        if not token in self._variables:
            self._variables.append(token)
        self.tokens.append(token)

    def add_str(self, string : str):
        self.tokens.append(CommandStringToken(string))