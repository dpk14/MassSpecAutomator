from Main.BackEnd.msp430.Library import commands

'''
Commands contain a string command and some parameters for that string and do not return anything.
'''

class Command:

    def __init__(self, command, parameters=None):
        self.command = command
        self.filled_command = self.set_command_parameters(parameters)
        self.executable = [self.filled_command]

    def get_strings(self):
        return self.executable

    #private_methods

    def set_command_parameters(self, parameters):
        if not self.parameters_valid(parameters):
            raise Exception
        try:
            if type(parameters) is not tuple:
                parameters = (parameters, )
        except:
            pass
        if parameters is not None:
            executable_command = commands.set_command_parameters(self.command, parameters)
        else:
            executable_command = self.command
        return executable_command

    '''
    parameters_valid is the only method you will implement for Command subclasses. Check out the other commands in this folder for
    further instructions
    '''

    def parameters_valid(self, parameter):
        return True