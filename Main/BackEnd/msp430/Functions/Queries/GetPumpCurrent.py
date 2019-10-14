import Main.BackEnd.msp430.Library.commands as commands
from Main.BackEnd.msp430.Functions.Queries.Query import Query


class GetPumpCurrent(Query):

    def __init__(self, pump_address):
        super().__init__(command=commands.PUMP_CURRENT, parameters=pump_address)

    def parse(self, response):
        pump_current = int(response[15: 18])
        pump_current = pump_current * .01
        return pump_current