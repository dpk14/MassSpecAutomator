from Main.BackEnd.msp430.Functions.Commands.CommandList import CommandList
from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Library import commands

class DeactivateTurbo(CommandList):

    def __init__(self):
        end = Command(commands.TURBO_END)
        power_off = Command(commands.TURBO_POWER_OFF)
        executable_commands = [end, power_off]
        super().__init__(executable_commands)
