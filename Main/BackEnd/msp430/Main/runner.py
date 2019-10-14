from Main.BackEnd.msp430.Communicator.main import msp430Communicator
from Main.BackEnd.msp430.Functions.Commands import AdjustPWMVoltage
from Main.BackEnd.msp430.Functions.Commands.ActivateTurbo import ActivateTurbo
from Main.BackEnd.msp430.Functions.Queries.GetVoltages import GetVoltages


#If something is underlined in red, click on it then hit alt-Enter and select where you want to import the module from

communicator = msp430Communicator()
communicator.connect()

command = ActivateTurbo()
communicator.execute(command=command)