from Main.BackEnd.msp430.Functions.Commands.CommandList import CommandList
from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Library import commands

class ActivateTurbo(CommandList):

    def __init__(self):
        power_on = Command(commands.TURBO_POWER_ON)
        start = Command(commands.TURBO_START)
        executable_commands = [power_on, start]
        super().__init__(executable_commands)
