from Main.BackEnd.msp430.Functions.Queries.Query import Query

import Main.BackEnd.msp430.Library.commands as commands

class TurboOn(Query):

    def __init__(self):
        super().__init__(command=commands.PUMP_STATUS)

    def parse(self, response):
        response = response.split(" ")
        turbo_status = response[7]
        return turbo_status == "On"
