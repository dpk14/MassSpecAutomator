import os
import sys

#IGNORE THIS

def get_port_config_file(self):
    return self.Config.get('Serial', 'port')

def get_baudrate_config_file(self):
    new_baudrate = self.Config.get('Serial', 'baudrate')
    if new_baudrate not in self.baudrates:
        print('Error: Unsupported baudrate, using default of 115200.')
        return self.baudrates[0]
    else:
        return new_baudrate

def check_config_file(self):
    f = self.Config.read(self.config_file)
    if f != [self.config_file]:
        print('Config file does not exist.  Creating ...')
        self.gen_config_file()
        print('Done')

    # Serial
    if self.Config.sections() != self.config_sections:
        print("Malformed config file. Regenerating ...")
        try:
            os.remove(self.config_file)
            self.gen_config_file()
        except:
            print("Error: " + str(sys.exc_info()))

def gen_config_file(self):
    cfgfile = open(self.config_file, 'w')
    self.Config.add_section('Serial')
    self.Config.set('Serial', 'port', self.default_port)
    self.Config.set('Serial', 'baudrate', self.baudrates[0])
    self.Config.write(cfgfile)
    cfgfile.close()

def save_config_file(self):
    print("Saving config file ...")
    try:
        cfgfile = open(self.config_file, 'w')

        self.Config.set('Serial', 'port', self.ser.port)
        self.Config.set('Serial', 'baudrate', self.ser.baudrate)
        self.Config.write(cfgfile)
        cfgfile.close()
        print('Done')
    except:
        print('Error' + str(sys.exc_info()))

'''
def on_load_gain_file(self, event):
    status = 'Error'
    print('Reading Gain File...')

    file_choices = "TXT (*.txt)|*.txt"
    dlg = wx.FileDialog(self, message="Load Gain File...", defaultDir=os.getcwd(), defaultFile="gain_file.txt",
                        wildcard=file_choices, style=wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
        raw_gain_array = np.genfromtxt(dlg.GetPath(), dtype=str)
        gain_array = ''.join(raw_gain_array)
        # print("len(gain_array): ", len(gain_array)
        # print("gain_array: " + gain_array
        # print("serial message: " + '\x10\x02GF' + gain_array + '\x10\x03'
    self.ser.write(str.encode('\x10\x02GF' + gain_array + '\x10\x03'))
    time.sleep(0.1)
    val = self.ser.read(3).decode(ENCODING)
    # if (len(val) == 3):
    # print("len(val) == 3"
    if (val != '\x06GF'):
        print("val: ", val)
        print("error\nImproper acknowledgment of GF Command:")
        self.ser.timeout = self.default_timeout
        self.ser.readlines()
    else:
        print('OK')
        status = 'OK'
    return status
'''