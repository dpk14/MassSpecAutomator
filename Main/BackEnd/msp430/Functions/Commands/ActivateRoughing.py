from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Library import commands

class ActivateRoughing(Command):

    def __init__(self):
        command = commands.ROUGH_PUMP_ON
        super().__init__(command=command)
