from Main.BackEnd.msp430.Communicator.main import msp430Communicator
from Main.BackEnd.msp430.Functions.Commands import AdjustPWMVoltage
from Main.BackEnd.msp430.Functions.Queries.GetVoltages import GetVoltages

#Do not change, keep as example, always name new file

'''
Step 1: instance the communicator.
Step 2: connect the communicator. Will break if device is not attached.
Step 3: instance a command or query and fill its parameters. Functions are located in the Functions package.
Step 4: perform communicator.execute(command) if you want to perform a command, or communicator.query(query) if you want
to make a query (if you want to get information from the device)
'''

communicator = msp430Communicator()
communicator.connect()

query = GetVoltages()
result = communicator.query(query=query)

command = AdjustPWMVoltage(percent=.1)
communicator.execute(command=command)

'''
Check out the Query superclass and Command superclass for information on how to create each.
'''