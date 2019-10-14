from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Library import commands

class DeactivateRoughing(Command):

    def __init__(self):
        command = commands.ROUGH_PUMP_OFF
        super().__init__(command=command)
