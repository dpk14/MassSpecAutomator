from Main.BackEnd.msp430.Functions.Queries.Query import Query

import Main.BackEnd.msp430.Library.commands as commands

class DetectorOn(Query):

    def __init__(self):
        super().__init__(command=commands.ARIZONA_STATUS)

    def parse(self, response):
        response = response.split(" ")
        state = response[4]
        return state == "On"
