import Main.BackEnd.msp430.Library.commands as commands
from Main.BackEnd.msp430.Functions.Commands.Command import Command

class AdjustPWMVoltage(Command):

    def __init__(self, percent):
        super().__init__(command=commands.ADJUST_PWM_VOLTS, parameters=percent)

    def parameters_valid(self, parameters):
        return 0 <= int(parameters[0]) <= 9