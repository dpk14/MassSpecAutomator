from Main.BackEnd.msp430.Functions.Queries.Query import Query
import Main.BackEnd.msp430.Library.commands as commands


class GetPumpPressure(Query):

    def __init__(self, pump_address):
        super().__init__(command=commands.PUMP_PRESSURE, parameters=pump_address)

    def parse(self, response):
        pressure_front = int(response[12: 16])
        pressure_exp = int(response.substring[16: 18]) - 20
        pressure = pressure_front * 0.001 * pow(10.0, pressure_exp) *0.750062
        return pressure