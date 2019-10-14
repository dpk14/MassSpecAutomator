from Main.BackEnd.Detector import defaults, plotter
#DataManager: used for getting data from the detector
#defaults: Just a long list of default settings for the detector

from Main.BackEnd.Detector.communicator import DetectorCommunicator

'''
Step 1: make a communicator. You can use these default parameters or assign your own. Then Connect.
'''

communicator = DetectorCommunicator(port=defaults.DEFAULT_PORT, baud_rate=defaults.DEFAULT_BAUDRATE, timeout=defaults.DEFAULT_TIMEOUT,
                 acq_delay=defaults.DEFAULT_DELAY)
communicator.connect()

'''
Step 2: take a spectrum. Again, you can use these defaults or assign your own.
'''

raw_data, data = communicator.take_spectrum(num_acqs=defaults.DEFAULT_ACQS, gain=defaults.DEFAULT_GAIN)

'''
Step 3: plot the data. The plotter script in this package is optional; it is primarily just used for testing. 
You can also create your own front end plotter script that plots the data on graphs that can be embedded into an interface.  
'''

plotter.draw_spectrum(data=data)
plotter.draw_raw_data(data=raw_data)

#To find out how to make libraries for a device, check the Library.Keithley module, especially the commands.py script.
#To find out how to make a function subclass, check the Functions directory and look at the Function.py script