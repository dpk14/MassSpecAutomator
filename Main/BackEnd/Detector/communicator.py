import serial

from Main.BackEnd.Detector import defaults, data_manager

#DONT MODIFY UNLESS BROKEN

class DetectorCommunicator:
    def __init__(self, port=defaults.DEFAULT_PORT, baud_rate=defaults.DEFAULT_BAUDRATE, timeout=defaults.DEFAULT_TIMEOUT,
                 acq_delay = defaults.DEFAULT_DELAY):
        self.port = port
        self.baud_rate = baud_rate
        self.default_timeout = timeout
        self.acq_delay = acq_delay

    def connect(self):
        ser = serial.Serial()
        if ser.isOpen():
            ser.Close()

        ser.port = self.port
        ser.baudrate = self.baud_rate
        ser.timeout = self.default_timeout
        try:
            print("Opening serial port ...")
            ser.open()
            print("OK")
        except:
            print("Error\nCould not open serial port")
            raise Exception
        self.ser = ser


    def send_serial_cmd(self, str):
        self.ser.write(str.encode('\x10\x02' + str + '\x10\x03'))
        val = self.ser.readlines()
        return val

    def set_gain(self, gain):
        status = 'Error'
        #print('Setting Gain to ' + self.gains[gain] + ' ...')
        self.ser.write(str.encode('\x10\x02AG' + str(gain) + '\x10\x03'))
        val = self.ser.read(3).decode(defaults.ENCODING)
        if (val != '\x06AG'):
            print("Error\nImproper acknowledgment of AG Command:")
            self.ser.timeout = self.default_timeout
            self.ser.readlines()
        else:
            print('OK')
            status = 'OK'
        return status

    def set_num_acqs(self, num_acqs):
        status = 'Error'
        print("Setting Number of Acquisitions to ")
        print(str(num_acqs) + ' ...')
        self.ser.write(str.encode('\x10\x02NR' + str(num_acqs) + '\x10\x03'))
        val = self.ser.read(3).decode(defaults.ENCODING)
        print(val)
        if (val != '\x06NR'):
            print("Error\nImproper acknowledgment of NR Command: " + str(val))
            self.ser.timeout = self.default_timeout
            self.ser.readlines()
        else:
            print("OK")
        return status

    def take_spectrum(self, num_acqs, gain):
        self.set_num_acqs(num_acqs=num_acqs)
        self.set_gain(gain=gain)
        manager = data_manager.DataManager(ser=self.ser, num_acqs=num_acqs, acq_delay=self.acq_delay,
                                           timeout=self.default_timeout,
                                           baud_rate=self.baud_rate)
        raw_data = manager.acquire_raw_data()
        data = manager.acquire_spectrum()
        return raw_data, data
