import struct
import time
import numpy as np

from Main.BackEnd.Detector import defaults

ENCODING='windows-1252'

#DONT MODIFY UNLESS BROKEN


class DataManager:
    def __init__(self, ser, num_acqs, acq_delay, timeout, baud_rate, num_pixels=defaults.DEFAULT_NUM_PIXELS,
                 supported_pixels = defaults.SUPPORTED_PIXELS):
        self.ser = ser
        self.num_pixels = num_pixels
        self.num_acqs = int(num_acqs)
        self.acq_delay = acq_delay
        self.timeout = timeout
        self.baud_rate = baud_rate
        self.supported_pixels = supported_pixels

    def acquire_raw_data(self):
        t1 = time.time()
        raw_data = np.zeros((self.num_acqs*self.num_pixels,))
        self.ser.write(str.encode('\x10\x02RD\x10\x03'))
        tint = self.num_acqs*self.acq_delay*41e-6
#       print("Integration Time: " + str(tint) + "s"

        twait = time.time()
        while ((self.ser.inWaiting() < 9) and ((time.time() - twait) <= 3*tint)):
            time.sleep(0.1)
        val = self.ser.read(9).decode(ENCODING)
        if len(val) == 9:
            new_num_pixels = 256*ord(val[2])+ord(val[3])
            new_num_acqs = ord(val[5])
            if ((str(new_num_pixels) not in defaults.SUPPORTED_PIXELS) or (new_num_acqs != self.num_acqs)):
                if (str(new_num_pixels) not in self.supported_pixels):
                    print("Error\nUnexpected Number of pixels: " + str(new_num_pixels))
                if (new_num_acqs != self.num_acqs):
                    print("Error\nUnexpected Number of Acquisitions: " + str(new_num_acqs))
            else:
                num_vals = new_num_acqs*self.num_pixels
                print("num_vals:", num_vals)
                if self.ser.timeout <= self.timeout:
                    self.ser.timeout = 2*num_vals*32/float(self.baud_rate)
                val = self.ser.read(4*num_vals)
                self.ser.read(1)
                val2 = self.ser.read(4)
                self.ser.read(5)
                if (len(val) == 4*num_vals):
                    for j in range(num_vals):
                        raw_data[j] = struct.unpack('>I',val[4*j:4*j+4])[0]
                        #print("self.raw_data[j]:", self.raw_data[j])
                else:
                    print("Error: Not enough recieved data.")
                #self.raw_data = self.raw_data[::-1]
                print("Data Acquisition Time: " + str(time.time()-t1))
                status = 'OK'
        elif len(val) == 0:
            print("Error\nNo response from camera")
        else:
            print("Error\nIncorrect response from camera: " + str(val))
        raw_data = np.reshape(raw_data,(self.num_pixels,-1), 'F')
        raw_data_x = np.arange(self.num_acqs)
        # calculate the mean and variance for each detector side for only the 1st acquisition
        odd_mean_value = np.mean(raw_data[1:self.num_pixels:2])
        odd_variance_value = np.var(raw_data[1:self.num_pixels:2])
        even_mean_value = np.mean(raw_data[0:self.num_pixels:2])
        even_variance_value = np.var(raw_data[0:self.num_pixels:2])
        # call the function to update the mean and variance outputs
        #self.get_st_mean_variance()
        # call the function to update the temperature
        #self.get_st_temp()
        # perform autosave if the checkbox is checked
        #if (self.autosave_flag == 1):
        #    self.autosave()
        return raw_data

    def acquire_spectrum(self):
                t1 = time.time()
                self.ser.write(str.encode('\x10\x02SD\x10\x03'))
                tint =self.num_acqs*self.acq_delay*41e-6
                print("Integration Time: " + str(tint) + "s")

                twait = time.time()
                while ((self.ser.inWaiting() < 9) and ((time.time() - twait) <= 3*tint)):
                        time.sleep(0.1)

                val = self.ser.read(9).decode(ENCODING)

                data = np.zeros((self.num_pixels,))
                if len(val) == 9:
                        new_num_pixels = 256*ord(val[2])+ord(val[3])
                        new_num_acqs = ord(val[5])
                        if ( (str(new_num_pixels) not in self.supported_pixels) or (new_num_acqs != 1)):
                                if (str(new_num_pixels) not in self.supported_pixels):
                                        print("Error\nUnexpected Number of pixels: " + str(new_num_pixels))
                                if (new_num_acqs != 1):
                                        print("Error\nUnexpected Number of Acquisitions:" + str(new_num_acqs))
                        else:
                                num_vals = new_num_acqs*self.num_pixels
                                if self.ser.timeout <= self.timeout:
                                        self.ser.timeout = 2*num_vals*32/float(self.baud_rate)

                                val = self.ser.read(4*num_vals)
                                self.ser.read(1)
                                val2 = self.ser.read(4)
                                self.ser.read(5)
                                if (len(val) == 4*self.num_pixels):
                                        for j in range(self.num_pixels):
                                                data[j] = struct.unpack('>i',val[4*j:4*j+4])[0]
                                                #print("Pixel "+ str(j) + " is = " + str(self.data[j])
                                else:
                                        print("Error\nNot enough received data.")
                                data = data[::-1]
                                data_raw = data
                                maximum = max(data)
                                data_norm = data/maximum*10;
                                print("Data Acquisition Time: " + str(time.time()-t1))
                                status = 'OK'

                elif len(val) == 0:
                        print("Error\nNo response from camera")
                else:
                        print("Error\nIncorrect response from camera: " + val)
                # perform autosave if the checkbox is checked
                #print("self.data array is: " + str(self.data)
                #self.data = np.flipud(self.data)
        #self.data_raw = self.data
                #self.max = max(self.data)
                #self.data = self.data/self.max*100;
                #print("self.data array is after flipud: " + str(self.normdata)
                self.save_data(data)
                return data

    def save_data(self, data):
        pass