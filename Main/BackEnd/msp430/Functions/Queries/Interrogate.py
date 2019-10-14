from Main.BackEnd.msp430.Functions.Queries.Query import Query
from Main.BackEnd.msp430.Library import commands


class Interrogate(Query):
    def __init__(self):
        super().__init__(command=commands.INTERROGATE)