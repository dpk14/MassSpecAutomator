from Main.BackEnd.GPIB_Device.Functions.SrcVoltsGetCurrent import SrcVoltsGetCurrent
from Main.BackEnd.GPIB_Device.Communicator.device_manager import GPIB_Device
from Main.BackEnd.GPIB_Device.Library import lib_names

#import library names so you know what device libraries have been built in
#library names so far: "Keithley", Agilent"

'''
Step 1: create the device using an ID and a device type. Device type is the name of the device's library.
Step 2: instance a function and fill its parameters. Functions are located in the Functions package.
Step 3: perform device.execute(function) and get result. Do what you please with this result.
'''

device = GPIB_Device(id=1, device_type=lib_names.KEITHLEY)
func = SrcVoltsGetCurrent(compliance="1e-5", voltage=10, current_range="20e-6")
result = device.execute(function=func)

'''
Go to Function package to find out how to make a Function
'''