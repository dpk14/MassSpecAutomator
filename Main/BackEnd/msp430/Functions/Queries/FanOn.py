from Main.BackEnd.msp430.Functions.Queries.Query import Query

import Main.BackEnd.msp430.Library.commands as commands

class FanOn(Query):

    def __init__(self):
        super().__init__(command=commands.TE_STATUS)

    def parse(self, response):
        response = response.split(" ")
        print(response)
        fan_status = response[5]
        return fan_status == "On"
