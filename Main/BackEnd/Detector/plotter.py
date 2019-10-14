import time

import numpy as np
from matplotlib.figure import Figure

from Main.BackEnd.Detector import defaults
import matplotlib.pyplot as plt
DPI = 100
FIGWIDTH = 10
FIGHEIGHT = 3.75
TITLE_SIZE = 10
LABEL_SIZE = 9

#this is just default plotting info copied over from the original detector code

def draw_raw_data(raw_data, num_acqs=defaults.DEFAULT_ACQS, cb_units=True, channels_odd = True, dt = defaults.DT, adu=defaults.ADU, dpi=DPI, grid_on=True):
    """ Redraws the figure """

    raw_data_x = np.arange(int(num_acqs))

    print(raw_data)
    print(raw_data_x)
    # clear the axes and redraw the plot anew
    if raw_data.shape[1] == raw_data_x.shape[0]:
        tstart = time.time()

        plt.grid(grid_on)
        if channels_odd:
            if cb_units:
                plt.plot(raw_data_x, raw_data[1::2].T)
            else:
                plt.plot(raw_data_x * dt, raw_data[1::2].T / adu)
        elif not channels_odd:
            if cb_units:
                plt.plot(raw_data_x, raw_data[0::2].T)
            else:
                plt.plot(raw_data_x * dt, raw_data[0::2].T / adu)
        else:
            # print("self.raw_data_x:", self.raw_data_x
            # print("self.raw_data.T:\n", self.raw_data.T
            if cb_units:
                plt.plot(raw_data_x, raw_data.T)
            else:
                plt.plot(raw_data_x * dt, raw_data.T / adu)
        print('Ploting Time:', time.time() - tstart, 's')
    else:
        print("Error\nIncorrect data length.")
    autosave()
    plt.show()

def draw_spectrum(data, num_pixels=defaults.DEFAULT_NUM_PIXELS, cb_units=True, adu=defaults.ADU, dpi=DPI, grid_on = True):
    """ Redraws the figure """
    # clear the axes and redraw the plot anew

    spectrum_x = np.arange(num_pixels)
    if (data.shape[0] == spectrum_x.shape[0]):
        tstart = time.time()
        plt.grid(grid_on)
        scale = 0.1
        if not cb_units:
            scale = scale * adu
        plt.plot(spectrum_x, data / scale, 'b-')
        # SETS THE AXES BOUNDS - NOT FROM ORIGINAL CODE - CHECK ORIGINAL FOR AUTOSCALE
        #plt.set_xbound((0, 1705))
        # self.axes.set_ylim(ymin = -10)
        # self.axes.set_ybound( (-5000,10000) )
        print('Ploting Time:', time.time() - tstart, 's')
    else:
        print("Error\nIncorrect data length.")
    autosave()
    plt.show()

def autosave(self):
#   path_data = "Acquire_Data_" + self.gains[self.gain] + datetime.datetime.fromtimestamp(time.time()).strftime('_%Y-%m-%d_%H-%M-%S-%f')
#   out_data = np.zeros((self.data.shape[0],))
    path_data = "Acquire_Data_" + str(time.time()-1500854400) + ".txt"
    out_data = self.data_raw
    np.savetxt(path_data, out_data.T, fmt='%d', delimiter='\t')