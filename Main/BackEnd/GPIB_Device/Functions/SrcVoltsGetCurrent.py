from Main.BackEnd.GPIB_Device.Functions.Function import Function

class SrcVoltsGetCurrent(Function):

    def __init__(self, voltage, compliance="1e-5", current_range="20e-6"):
        inputs = [compliance, voltage, current_range]
        super().__init__(inputs) #copy this over for all subclasses

    def write_commands_from_libraries(self, command_lib, query_lib, keyword_lib):
        COMMANDS = (command_lib.SET_COMPLIANCE, command_lib.SRC_VOLTS, command_lib.SET_CURRENT_RANGE)
        return COMMANDS
