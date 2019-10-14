import threading
from tkinter import ttk
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Main.BackEnd.Detector import defaults
import Main.GUI.Tools.display_tools as tools
from Main.BackEnd.Detector.communicator import DetectorCommunicator
from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Functions.Queries.DetectorOn import DetectorOn
from Main.BackEnd.msp430.Library import commands
from Main.GUI.Widgets.Steps.Step import Step
from Main.GUI.Tools import plotter

PORT = "Com Port: "
BAUDRATE = "Baud Rate: "
TIMEOUT = "Timeout: "
ACQ_DELAY = "Acquisition Delay: "
ACQS = "Acquisitions: "
GAIN = "Gain: "

ON_BUTTON = "Turn Arizona Detector "
TURN_ON = ON_BUTTON + "ON"
TURN_OFF = ON_BUTTON + "OFF"
TAKE_SPECTRUM = "Take Spectrum"

CONNECT = "Connect"
DISCONNECT = "Disconnect"

COULD_NOT_CONNECT_ERROR = "Could not connect! Check your Device Manager to ensure the COM port name is correct."

TITLES = [PORT, BAUDRATE, TIMEOUT, ACQ_DELAY]
DEFAULTS = {
            PORT: defaults.DEFAULT_PORT,
            BAUDRATE: defaults.DEFAULT_BAUDRATE,
            TIMEOUT: defaults.DEFAULT_TIMEOUT,
            ACQ_DELAY: defaults.ACQ_DELAY,
            ACQS: defaults.DEFAULT_ACQS,
            GAIN: defaults.DEFAULT_GAIN
            }

class DetectorDisplay(Step):

    FIELDS_NEEDED = ()

    def __init__(self, win, outer_frame, communicator, console):
        self.win = win
        self.communicator = communicator
        self.outer_frame = outer_frame
        self.frame = ttk.LabelFrame(self.outer_frame, text="Step 5: Detector")
        self.frame.pack(side=tk.LEFT)
        self.console = console
        self.fig = None
        self.fill_interface()
        super().__init__(self.frame)

    def set_update_flags(self, update_spectrum, spectrum_updated):
        self.update_spectrum = update_spectrum
        self.spectrum_updated = spectrum_updated

    def fill_interface(self):
        tools.create_blank_rows(self.frame)
        frame1 = ttk.Frame(self.frame)
        frame1.pack(side=tk.TOP)
        self.on_button = ttk.Button(frame1, text=TURN_ON, state=tk.DISABLED, command=lambda activated=False: self.detector_on(already_activated=activated))
        self.on_button.pack(side=tk.LEFT, anchor=tk.CENTER)

        tools.create_blank_rows(self.frame)
        frame2 = ttk.LabelFrame(self.frame, text="Connect")
        frame2.pack(side=tk.TOP)
        entryframe = ttk.Frame(frame2)
        entryframe.pack(side=tk.TOP)
        self.entry_map = self.make_communicator_entries(entryframe)
        buttframe = ttk.Frame(frame2)
        buttframe.pack(side=tk.TOP)
        self.com_button = ttk.Button(buttframe, text="Connect", state="disabled", command=lambda frame=frame2: self.detector_connect(frame))
        self.com_button.pack(side=tk.TOP, anchor=tk.CENTER)

        tools.create_blank_rows(self.frame)
        self.make_spectrum_frame()

    def make_spectrum_frame(self):
        detec_frame = ttk.LabelFrame(self.frame, text="Take Spectrum")
        detec_frame.pack(side=tk.TOP)

        entry_frame = ttk.Frame(detec_frame)
        entry_frame.pack(side=tk.TOP)

        tools.create_blank_rows(entry_frame)
        acq_label = ttk.Label(entry_frame, text="Acquisitions: ")
        acq_label.pack(side=tk.LEFT)
        self.acq_entry = ttk.Entry(entry_frame)
        self.acq_entry.pack(side=tk.LEFT)
        self.acq_entry.insert(tk.END, DEFAULTS[ACQS])
        self.acq_entry.configure(state="disabled")

        gain_label = ttk.Label(entry_frame, text="Gain: ")
        gain_label.pack(side=tk.LEFT)
        self.gain_entry = ttk.Entry(entry_frame)
        self.gain_entry.pack(side=tk.LEFT)
        self.gain_entry.insert(tk.END, DEFAULTS[GAIN])
        self.gain_entry.configure(state="disabled")
        tools.create_blank_rows(entry_frame)

        self.canvas_frame = ttk.Frame(detec_frame)
        self.canvas_frame.pack(side=tk.TOP)

        button_frame = ttk.Frame(detec_frame)
        button_frame.pack(side=tk.TOP)

        tools.create_blank_rows(button_frame)
        self.spectrum_button = ttk.Button(button_frame, text=TAKE_SPECTRUM, state="disabled", command=self.run)
        self.spectrum_button.pack(side=tk.TOP, anchor=tk.CENTER)
        tools.create_blank_rows(button_frame)

    def make_communicator_entries(self, frame):
        entry_map = {}
        halfway = int(len(TITLES)/2)
        for index in range(len(TITLES)):
            if index == 0 or index == halfway:
                column = ttk.Frame(frame)
                column.pack(side=tk.LEFT)
            subframe = ttk.Frame(column)
            subframe.pack(side=tk.TOP)
            title = TITLES[index]
            label = ttk.Label(subframe, text=title)
            label.pack(side=tk.LEFT)
            entry = ttk.Entry(subframe)
            entry.pack(side=tk.LEFT)
            default = DEFAULTS[title]
            entry.insert(tk.END, default)
            entry.configure(state=tk.DISABLED)
            entry_map[title] = entry
            tools.create_blank_rows(column)
        tools.create_blank_rows(frame)
        return entry_map

    def detector_on(self, already_activated=False):
        if self.on_button['text'] == TURN_ON:
            self.com_button.configure(state="normal")
            self.on_button['text'] = TURN_OFF
            for key in self.entry_map.keys():
                entry = self.entry_map[key]
                entry.configure(state=tk.NORMAL)
            if not already_activated:
                command = Command(commands.ARIZONA_POWER_ON)
                self.communicator.execute(command)
                self.console.display_command(command)
        else:
            self.on_button['text'] = TURN_ON
            command = Command(commands.ARIZONA_POWER_OFF)
            self.communicator.execute(command)
            self.console.display_command(command)
            self.com_button.configure(state="disabled")
            for key in self.entry_map.keys():
                entry = self.entry_map[key]
                entry.configure(state=tk.DISABLED)

    def detector_connect(self, frame):
        port = self.entry_map[PORT].get()
        baud_rate = self.entry_map[BAUDRATE].get()
        acq_delay = self.entry_map[ACQ_DELAY].get()
        timeout = self.entry_map[TIMEOUT].get()

        error_message = self.validate_connect_inputs(port, baud_rate, acq_delay)
        if error_message is not "":
            tools.display_error_box(error_message)
            return

        self.detector_com = DetectorCommunicator(port=port, baud_rate=int(baud_rate), timeout=float(timeout), acq_delay=float(acq_delay))
        try:
            self.detector_com.connect()
        except:
            tools.display_error_box(COULD_NOT_CONNECT_ERROR)
            return

        self.spectrum_button.configure(state="enabled")
        self.acq_entry.configure(state=tk.NORMAL)
        self.gain_entry.configure(state=tk.NORMAL)

    def run(self):
        calibration_thread = threading.Thread(target=self.update_graph, args=())
        calibration_thread.start()

    def update_graph(self):
        self.update_spectrum.set()
        self.spectrum_button.configure(text="Taking Spectrum...")
        self.spectrum_button.configure(state=tk.DISABLED)
        self.spectrum_updated.wait()
        self.spectrum_updated.clear()
        self.spectrum_button.configure(text=TAKE_SPECTRUM)
        self.spectrum_button.configure(state=tk.NORMAL)

    def take_spectrum(self):
        num_acqs = self.acq_entry.get()
        gain = self.gain_entry.get()
        raw_data, data = self.detector_com.take_spectrum(int(num_acqs), int(gain))
        return raw_data, data, num_acqs

    def clear(self, widget):
        for child in widget.winfo_children():
            child.destroy()

    def validate_connect_inputs(self, port_name, baudrate, acq_delay):
        if not (port_name[0:3] == "COM"):
            return "Faulty port name"
        try:
            int(port_name[3])
        except:
            return "Faulty port name"
        if not (baudrate in defaults.BAUDRATES):
            return "Faulty baudrate"
        if float(acq_delay) < 0:
            return "Invalid delay"
        return ""

    def activate(self):
        self.on_button.configure(state=tk.NORMAL)
        detector_on = self.communicator.query(DetectorOn())
        if detector_on:
            self.detector_on(already_activated=True)