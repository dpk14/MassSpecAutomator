from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Library import commands

class ActivateElectricSector(Command):

    def __init__(self):
        command = commands.ELEC_SEC_ON
        super().__init__(command=command)
