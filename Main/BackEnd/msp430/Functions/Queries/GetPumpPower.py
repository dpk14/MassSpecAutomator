from Main.BackEnd.msp430.Functions.Queries.Query import Query

import Main.BackEnd.msp430.Library.commands as commands

class GetPumpPower(Query):

    def __init__(self, pump_address):
        super().__init__(command=commands.PUMP_POWER, parameters=pump_address)

    def parse(self, response):
        pump_power = int(response[16: 18])
        return pump_power