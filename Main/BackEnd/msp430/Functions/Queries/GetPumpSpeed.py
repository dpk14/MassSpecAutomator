from Main.BackEnd.msp430.Functions.Queries.Query import Query
import Main.BackEnd.msp430.Library.commands as commands

class GetPumpSpeed(Query):

    def __init__(self, pump_address):
        super().__init__(command=commands.PUMP_SPEED, parameters=pump_address)

    def parse(self, response):
        speed = int(response[14: 18])
        return speed