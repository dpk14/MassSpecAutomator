from Main.BackEnd.msp430.Functions.Queries.Query import Query

import Main.BackEnd.msp430.Library.commands as commands

class RoughingOn(Query):

    def __init__(self):
        super().__init__(command=commands.PUMP_STATUS)

    def parse(self, response):
        response = response.split(" ")
        roughing_status = response[2]
        return roughing_status == "On"
