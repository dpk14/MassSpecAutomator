from Main.BackEnd.GPIB_Device.Functions.Function import Function
from Main.BackEnd.GPIB_Device.Library import errors


class SimpleSweep(Function):

    '''
    If you would like to implement the validate_inputs method, say self.parameter = parameter for each parameter the function
    receives. This 'saves' each input in the function as an instance variable so that you can validate each input later by name

    Most importantly, write out all the parameters in the order in which you'd like them to be used and store them as inputs.

    Ex:
    inputs = [parameter1, parameter2, parameter3]

    Lastly, say super().__init__(inputs) to build the internal superclass
    '''

    def __init__(self, start, end, step, delay, count, compliance):
        self.start = start
        self.end = end
        self.step = step
        self.delay = delay
        self.count = count
        self.compliance = compliance
        inputs = [compliance, start, end, step, count, delay]
        super().__init__(inputs) #This line is the same for every single subclass you will make

    '''
    Make a tuple or list and set it equal to an INITIALIZER, then return this INITIALIZER. An INITIALIZER is a sequence of 
    string commands that configure the device to perform your function. If the command takes a parameter, you can set that 
    parameter using command_lib.set_command_parameters(command, parameter). The user (the person calling your function)
    does not get to set the parameters for the INITIALIZER; the designer of the function builds in these parameters by default
    to save the user some extra work.     
    '''

    def write_initializer_from_libraries(self, command_lib, query_lib, keyword_lib):
        INITIALIZER = (
            command_lib.SRC_TO_VOLTS,
            command_lib.set_command_parameters(command_lib.commands.CURRENT_TYPE, keyword_lib.DC),
            command_lib.set_command_parameters(command_lib.commands.MODE, keyword_lib.SWE),
            command_lib.set_command_parameters(command_lib.commands.RANGE, keyword_lib.AUTO),
            command_lib.set_command_parameters(command_lib.commands.SPAC, keyword_lib.LIN)
        )
        return INITIALIZER

    '''
       Make a tuple or list and set it equal to COMMANDS, then return this COMMANDS variable. COMMANDS are a sequence of 
       string commands that require parameters from the user. There MUST be a one-to-one, ordered mapping between your parameters and
       your COMMAND list. For instance, the parameters of this Function subclass are:
       
       [compliance, start, end, step, count, delay]
       
       ...and the COMMANDS are:
       
       [SET_COMPLIANCE, START, STOP, STEP, COUNT, DELAY]
       
       Notice how the commands map directly to their parameters 
       '''

    def write_commands_from_libraries(self, command_lib, query_lib, keyword_lib):
        COMMANDS = (command_lib.SET_COMPLIANCE, command_lib.START, command_lib.STOP, command_lib.STEP,
                         command_lib.COUNT, command_lib.DELAY)
        return COMMANDS

    '''
        Make a bunch of conditionals and return an error associated with each.
    '''

    def validate_inputs(self):
        if self.delay < 0:
            return errors.NEG_DELAY_ERROR
        if ((self.end - self.start) * self.step < 0) or (self.step == 0 and (abs(self.start - self.end) > 0)):
            return errors.INFINITE_COUNT_ERROR
        if abs(self.end) > errors.MAX_VOLTS:
            return errors.MAX_VOLTAGE_EXCEEDED
        if abs(self.compliance) > errors.MAX_COMPLIANCE:
            return errors.MAX_COMPLIANCE_EXCEEDED
        return ""
