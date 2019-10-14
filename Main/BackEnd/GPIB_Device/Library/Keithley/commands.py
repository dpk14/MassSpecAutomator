'''
To add a new command, write out the string and replace the location you would like to substitute with ARGS[num], where num
is the argument number
'''


ARGS = ["ARG1", "ARG2", "ARG3"]

#0 Parameters
SRC_TO_VOLTS = ":SOUR:FUNC VOLT"
OUTPUT_ON = ":OUTP ON"
OUTPUT_OFF = ":OUTP OFF"

#1 Parameter
SRC_VOLTS = ":SOUR:VOLT " + ARGS[0]
CURRENT_TYPE = ":SENS:FUNC " + ARGS[0]
SET_COMPLIANCE = "SENS:CURR:PROT " + ARGS[0]
SET_CURRENT_RANGE = ":SENS:CURR:RANG " + ARGS[0]
START = ":SOUR:VOLT:START " + ARGS[0]
STOP = ":SOUR:VOLT:STOP " + ARGS[0]
STEP = ":SOUR:VOLT:STEP " + ARGS[0]
MODE = ":SOUR:VOLT:MODE " + ARGS[0]
RANGE = ":SOUR:SWE:RANG " + ARGS[0]
SPAC = ":SOUR:SWE:SPAC " + ARGS[0]
COUNT = ":TRIG:COUN " + ARGS[0]
DELAY = ":SOUR:DEL " + ARGS[0]

def set_command_parameters(command, parameters):
    executable_command = ""
    for arg_index in range(len(parameters)):
        ARG_PLACEHOLDER = ARGS[arg_index]
        parameter = parameters[arg_index]
        executable_command = command.replace(ARG_PLACEHOLDER, str(parameter))
    return executable_command