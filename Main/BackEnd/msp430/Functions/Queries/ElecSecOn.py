from Main.BackEnd.msp430.Functions.Queries.Query import Query

import Main.BackEnd.msp430.Library.commands as commands

class ElecSecOn(Query):

    def __init__(self):
        super().__init__(command=commands.ELEC_SEC_STATUS)

    def parse(self, response):
        state = response.split(" ")[3]
        return state == "On"
