from Main.BackEnd.GPIB_Device.Library.Keithley import commands, queries, keywords
from Main.BackEnd.GPIB_Device.Library.Agilent import commands, queries, keywords

#Skip down to the last three methods. These are the only methods a Function subclass will implement.

class Function:

    INPUTS_INVALID = "Inputs are invalid"

    def __init__(self, inputs):
        try:
            self.validate_inputs()
            self.inputs = inputs
        except:
            raise Exception(self.INPUTS_INVALID)

    def get_commands(self, library):
        command_lib = library.commands
        query_lib = library.queries
        keyword_lib = library.keywords
        INITIALIZER = self.write_initializer_from_libraries(command_lib, query_lib, keyword_lib)
        COMMANDS = self.write_commands_from_libraries(command_lib, query_lib, keyword_lib)
        COMMAND_ARGS_MAP = self.initialize_command_args_map(COMMANDS, self.inputs)
        executable_commands = self.set_command_parameters(COMMAND_ARGS_MAP, command_lib)
        all_commands = INITIALIZER + executable_commands
        return all_commands

    #private methods

    def initialize_command_args_map(self, COMMANDS, inputs):
        args_map = {}
        for index in range(len(COMMANDS)):
            COMMAND = COMMANDS[index]
            if type(inputs[index]) == tuple:
                parameters = inputs[index]
            else:
                parameters = (inputs[index], )
            args_map[COMMAND] = parameters
        return args_map

    def set_command_parameters(self, COMMAND_ARGS_MAP, command_lib):
        executable_commands = ()
        for COMMAND in COMMAND_ARGS_MAP.keys():
            parameters = COMMAND_ARGS_MAP[COMMAND]
            executable_command = command_lib.set_command_parameters(COMMAND, parameters)
            executable_commands+=(executable_command, )
        return executable_commands

    '''
    The three methods below are to be implemented by your function subclass. You do not have to implement all of them. 
    If you would like to display an error if the user inputs an incorrect parameter, implement the validate_inputs method
    and return an appropriate error message for the incorrect ranges of each parameter. To write out the list of commands with parameters
    you would like your custom Function subclass to use, implement write_commands_from_libraries. To write out the list of 0 parameter 
    initialization commands you would like your custom Function subclass to use, implement write_initializer_from_libraries.
    Check out SimpleSweep and SrcVoltsGetCurrent for examples of how to implement these methods. 
    '''

    def validate_inputs(self):
        pass

    def write_commands_from_libraries(self, command_lib, query_lib, keyword_lib):
        return ()

    def write_initializer_from_libraries(self, command_lib, query_lib, keyword_lib):
        return ()