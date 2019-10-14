import time

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Main.BackEnd.Detector import defaults
import matplotlib.pyplot as plt

from Main.Data.Spectrums.PathInfo import path_info

SAVE_PATH = path_info.SPECTRUM_DATA_PATH

DPI = 100
FIGWIDTH = 5
FIGHEIGHT = 3
TITLE_SIZE = 10
LABEL_SIZE = 9

#this is mostly copied over from the original detector code. I do not take responsibility for its design

def display_graphs(data, raw_data, num_acqs):
    draw_raw_data(raw_data=raw_data, num_acqs=num_acqs)
    draw_spectrum(data=data, num_pixels=defaults.DEFAULT_NUM_PIXELS)

def update_embedded_graph(canvas, axis, data, raw_data, num_acqs):
    #draw_raw_data_canvas(axis, raw_data=raw_data, num_acqs=num_acqs)
    draw_spectrum_canvas(canvas, axis, data=data, num_pixels=defaults.DEFAULT_NUM_PIXELS)
    return

def make_empty_graph(frame, fig_width=FIGWIDTH, fig_height=FIGHEIGHT):
    fig = Figure(figsize=(fig_width, fig_height))
    axis = fig.add_subplot(111)
    axis.plot([], [])
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack()
    canvas.draw()
    return canvas, axis


#I didn't write this! I just copied it over from the original detector code and slightly modified it for efficiency
def draw_raw_data_canvas(axis, raw_data, num_acqs, cb_units=True, channels_odd = True, dt = defaults.DT, adu=defaults.ADU, dpi=DPI, grid_on=True):
    """ Redraws the figure """

    #fig = plt.Figure((5.0, 4.0), dpi=dpi)
    #axes = fig.add_subplot(111)
    num_acqs = int(num_acqs)
    raw_data_x = np.arange(num_acqs)

    # clear the axes and redraw the plot anew
    if raw_data.shape[1] == raw_data_x.shape[0]:
        tstart = time.time()

        axis.grid(grid_on)
        if channels_odd:
            if cb_units:
                axis.plot(raw_data_x, raw_data[1::2].T)
            else:
                axis.plot(raw_data_x * dt, raw_data[1::2].T / adu)
        elif not channels_odd:
            if cb_units:
                axis.plot(raw_data_x, raw_data[0::2].T)
            else:
                axis.plot(raw_data_x * dt, raw_data[0::2].T / adu)
        else:
            # print("self.raw_data_x:", self.raw_data_x
            # print("self.raw_data.T:\n", self.raw_data.T
            if cb_units:
                axis.plot(raw_data_x, raw_data.T)
            else:
                axis.plot(raw_data_x * dt, raw_data.T / adu)
        print('Ploting Time:', time.time() - tstart, 's')
    else:
        print("Error\nIncorrect data length.")
    #plt.show()

#I didn't write this! I just copied it over from the original detector code and slightly modified it for efficiency
def draw_spectrum_canvas(canvas, axis, data, num_pixels, cb_units=True, adu=defaults.ADU, dpi=DPI, grid_on = True):
    """ Redraws the figure """
    # clear the axes and redraw the plot anew
    axis.clear()
    spectrum_x = np.arange(num_pixels)
    if (data.shape[0] == spectrum_x.shape[0]):
        tstart = time.time()
        axis.grid(grid_on)
        scale = 0.1
        if not cb_units:
            scale = scale * adu
        y = data/scale
        axis.set_ylim(min(spectrum_x), max(y))
        axis.semilogx(spectrum_x, y, 'b-')
        # SETS THE AXES BOUNDS - NOT FROM ORIGINAL CODE - CHECK ORIGINAL FOR AUTOSCALE
        #plt.set_xbound((0, 1705))
        # self.axes.set_ylim(ymin = -10)
        # self.axes.set_ybound( (-5000,10000) )
        print('Ploting Time:', time.time() - tstart, 's')
    else:
        print("Error\nIncorrect data length.")
    canvas.draw()
    #plt.show()


#I didn't write this! I just copied it over from the original detector code and slightly modified it for efficiency
def draw_raw_data(raw_data, num_acqs=defaults.DEFAULT_ACQS, cb_units=True, channels_odd=True, dt=defaults.DT,
                  adu=defaults.ADU, dpi=DPI, grid_on=True):
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
    autosave(raw_data, header="Raw_Data")
    plt.show()

#I didn't write this! I just copied it over from the original detector code and slightly modified it for efficiency
def draw_spectrum(data, num_pixels=defaults.DEFAULT_NUM_PIXELS, cb_units=True, adu=defaults.ADU, dpi=DPI, grid_on=True):
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
        # plt.set_xbound((0, 1705))
        # self.axes.set_ylim(ymin = -10)
        # self.axes.set_ybound( (-5000,10000) )
        print('Ploting Time:', time.time() - tstart, 's')
    else:
        print("Error\nIncorrect data length.")
    autosave(data, header="Spectrum_Data")
    plt.show()


def autosave(data, header="Acquire_Data_"):
    #   path_data = "Acquire_Data_" + self.gains[self.gain] + datetime.datetime.fromtimestamp(time.time()).strftime('_%Y-%m-%d_%H-%M-%S-%f')
    #   out_data = np.zeros((self.data.shape[0],))
    path_data = SAVE_PATH + "\\" + header + str(time.time() - 1500854400) + ".txt"
    out_data = data
    np.savetxt(path_data, out_data.T, fmt='%d', delimiter='\t')