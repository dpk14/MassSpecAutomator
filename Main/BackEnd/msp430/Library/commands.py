'''
To add a new command, write out the string and replace the location you would like to substitute with ARGS[num], where num
is the argument number
'''

ARGS = ["ARG1", "ARG2", "ARG3"]

#General
INTERROGATE = ".."
SET_TIME = "*"
GET_ANALOG_DIGITAL_SYST_DEFAULTS = ".AD"
GET_BUILD_DATE = ".R"
GET_SYST_DEFAULTS_L = ".L"
GET_SYST_DEFAULTS_V = ".V"
SUB_SYSTEM_STATUS = ".Y"
FIRMWARE_UPDATER = ".B"
SPI_TEST = ".U"

#Voltages
V_12_OFF = ".WP0"
V_12_ON = ".WP1"
V_12_STATUS = ".WS"

#Arizona
ARIZONA_POWER_ON = ".DP1"
ARIZONA_POWER_OFF = ".DP0"
ARIZONA_INIT_I_BUFF = ".DI"
ARIZONA_STATUS = ".DS"
ARIZONA_OPEN = ".DO"
ARIZONA_DATA_SCAN = ".DD"
ARIZONA_INIT_I_DATA_BUFF = ".DZ"

#Electric sector
ELEC_SEC_ON = ".EO1"
ELEC_SEC_OFF = ".EO0"
ELEC_SEC_STATUS = ".EOS"
ELEC_SEC_INIT = ".EI"
ELEC_SEC_STEP_CONFIG = ".EC"
ELEC_SEC_POS_V_STEP_SET = ".EP" + ARGS[0]
ELEC_SEC_NEG_V_STEP_SET = ".EN" + ARGS[0]

ELEC_SEC_POS_DOWN_1 = ".EDP1"
ELEC_SEC_POS_DOWN_10 = ".EDP2"
ELEC_SEC_POS_DOWN_100 = ".EDP3"

ELEC_SEC_NEG_DOWN_1 = ".EDN1"
ELEC_SEC_NEG_DOWN_10 = ".EDN2"
ELEC_SEC_NEG_DOWN_100 = ".EDN3"

ELEC_SEC_POS_UP_1 = ".EUP1"
ELEC_SEC_POS_UP_10 = ".EUP2"
ELEC_SEC_POS_UP_100 = ".EUP3"

ELEC_SEC_NEG_UP_1 = ".EUN1"
ELEC_SEC_NEG_UP_10 = ".EUN2"
ELEC_SEC_NEG_UP_100 = ".EUN3"

ELEC_SEC_POS_V_WRT_ADJ_STEPS = ".EWP" + ARGS[0]
ELEC_SEC_NEG_V_WRT_ADJ_STEPS = ".EWN" + ARGS[0]
ELEC_SEC_RD_STEP = ".EF"
ELEC_SEC_SET_MAX_VOLT = ".EM"
ELEC_SEC_SET_MIN_VOLT = ".ER"
ELEC_SEC_POTENT_SETTINGS = ".EV"


#Grid Voltages
GRID_VOLT_ON = ".GP1"
GRID_VOLT_OFF = ".GP0"
GRID_VOLT_STATUS = ".GS"
GRID_INIT = ".GI"
GRID_STEP_CONFIG = ".GC"
GRID_V_STEP_SET = ".G" + ARGS[0]
GRID_V_ADJ_DOWN = ".GD" + ARGS[0]
GRID_V_ADJ_UP = ".GU" + ARGS[0]
GRID_V_WRT_ADJ_STEPS = ".GW" + ARGS[0]
GRID_RD_STEP = ".GF"
GRID_MAX_VOLT = ".GM"
GRID_MIN_VOLT = ".GR"
GRID_POTENT_SETTINGS = ".GV"

#Source Voltage Control
SRC_V_ON = ".SP1"
SRC_V_OFF = ".SP0"
SRC_V_STEP = ".SC"
SRC_V_ADJ_DOWN = ".SD" + ARGS[0]
SRC_V_ADJ_UP = ".SU" + ARGS[0]
INIT_SRC_V = ".SI"
SRC_V_STATUS = ".SS"

#Pumps Control
ROUGH_PUMP_ON = ".PR1"
ROUGH_PUMP_OFF = ".PR0"
TURBO_POWER_ON = ".PT1"
TURBO_POWER_OFF = ".PT0"
TURBO_START = ".PG1"
TURBO_END = ".PG0"
PUMP_INIT = ".PI"
PUMP_STATUS = ".PS"

#PUMP commands:
PUMP_COMMAND = ".PC"
PUMP_SPEED = PUMP_COMMAND + "00" + ARGS[0] + "10030902=?107"
PUMP_PRESSURE = PUMP_COMMAND + "00" + ARGS[0] + "0074002=?106"
PUMP_CURRENT = PUMP_COMMAND + "00" + ARGS[0] + "0031002=?099"
PUMP_POWER = PUMP_COMMAND + "00" + ARGS[0] + "0031602=?105"

PUMP_COMMAND = ".PC00" + ARGS[0] + ARGS[1] #arg1 = address, arg2 is rest of string

#Therm Electric
THERM_ELEC_FAN_OFF = ".TF0"
THERM_ELEC_FAN_ON = ".TF1"
THERM_ELEC_V_OFF = ".TP0"
THERM_ELEC_V_ON = ".TP1"
TE_STATUS = ".TS"
ADJUST_PWM_VOLTS = ".TR" + ARGS[0]


def set_command_parameters(command, parameters):
    executable_command = ""
    for arg_index in range(len(parameters)):
        ARG_PLACEHOLDER = ARGS[arg_index]
        parameter = parameters[arg_index]
        executable_command = command.replace(ARG_PLACEHOLDER, str(parameter))
    return executable_command
