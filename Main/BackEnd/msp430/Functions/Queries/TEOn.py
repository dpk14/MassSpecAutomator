from Main.BackEnd.msp430.Functions.Queries.Query import Query

import Main.BackEnd.msp430.Library.commands as commands

class TEOn(Query):

    def __init__(self):
        super().__init__(command=commands.TE_STATUS)

    def parse(self, response):
        response = response.split(" ")
        te_status = response[3]
        return te_status == "On"
