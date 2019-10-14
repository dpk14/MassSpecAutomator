from Main.BackEnd.msp430.Functions.Commands.Command import Command

'''
Queries are just Commands that return a value, so they have an additional parse method which must be implemented
to determine how the msp430's response is translated into a readable output. 
'''

class Query(Command):

    def __init__(self, command, parameters=None):
        super().__init__(command, parameters)

    def parse(self, response):
        return response