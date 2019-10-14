import threading
import tkinter as tk
from tkinter import ttk

import ttkthemes as ttkthemes

from Main.BackEnd.msp430.Communicator import main
from Main.GUI.Widgets.Status import stats_panel, graph_panel
import Main.GUI.Controller.updater as com_controller
from Main.GUI.Widgets.Steps.connect import ConnectDisplay
from Main.GUI.Widgets.Steps.detector import DetectorDisplay
from Main.GUI.Widgets.Steps.electric_sector import ElectricSectorDisplay
from Main.GUI.Widgets.Steps.pump import PumpControl
from Main.GUI.Widgets.Steps.thermal_electric import ThermalElectricDisplay
from Main.GUI.Tools import display_tools
from Main.GUI.Widgets.Status.console import Console

STEP_CLASSES = [ConnectDisplay, PumpControl, ElectricSectorDisplay, ThermalElectricDisplay, DetectorDisplay]

class DisplayController:
    def __init__(self, win):
       self.initialize(win)

    def initialize(self, win):
        self.win = win
        self.communicator = main.msp430Communicator()

        main_frame = ttk.Frame(win)
        main_frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        step_frame, bottom_frame = self.make_subframes(main_frame)

        self.console = Console(bottom_frame, self.communicator)

        #fill_top_frame:
        self.STEPS = self.make_steps(step_frame)
        display_tools.create_blank_rows(step_frame)

        #fill_bottom_frame
        self.console.pack(side=tk.LEFT)
        self.stats_panel = stats_panel.StatsPanel(bottom_frame)
        self.stats_panel.pack(side=tk.LEFT)
        self.graph_panel = graph_panel.GraphPanel(win, bottom_frame)
        self.graph_panel.pack()

        #make update threads:
        connect_step = self.STEPS[0]
        self.connected = threading.Event()
        self.connect_button = connect_step.make_connect_button(self.connected)
        self.stats_panel.disable()

        self.connection_thread = threading.Thread(target=self.check_connection, args=())
        self.connection_thread.start()

        self.detector_step = self.STEPS[len(self.STEPS) - 1]
        self.update_spectrum = threading.Event()
        self.spectrum_updated = threading.Event()
        self.detector_step.set_update_flags(self.update_spectrum, self.spectrum_updated)

        self.graph_thread = threading.Thread(target=self.check_graph, args=())
        self.graph_thread.start()

        win.mainloop()

    def make_subframes(self, main_frame):
        display_tools.create_blank_rows(main_frame)

        step_frame = ttk.LabelFrame(main_frame, text="Steps")
        step_frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        display_tools.create_blank_rows(step_frame)
        display_tools.create_blank_rows(main_frame)

        bottom_frame = ttk.LabelFrame(main_frame, text="Status")
        bottom_frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        return step_frame, bottom_frame

    def make_steps(self, step_frame):
        STEPS = []
        for index in range(len(STEP_CLASSES)):
            step = STEP_CLASSES[index]
            step = step(win=self.win, outer_frame=step_frame, communicator=self.communicator, console=self.console)
            step.pack()
            display_tools.create_blank_cols(step_frame, 2)
            STEPS.append(step)
        return STEPS

    def activate(self):
        self.stats_panel.enable()
        self.console.activate()
        for step in self.STEPS:
            step.activate()
        self.loop = com_controller.LoopManager(main=self.win, communicator=self.communicator,
                                               stats_panel=self.stats_panel,
                                               connect_button=self.connect_button, connection_event=self.connected)
    def deactivate(self):
        self.communicator.disconnect()
        self.graph_thread.join()
        self.connection_thread.join()
        for widget in self.win.winfo_children():
            widget.destroy()
        self.initialize(self.win)

    def check_connection(self):
        self.connected.wait()
        self.activate()
        self.connected.clear()
        self.connected.wait()
        self.deactivate()

    def check_graph(self):
        while True:
            self.update_spectrum.wait()
            raw_data, data, num_acqs = self.detector_step.take_spectrum()
            self.graph_panel.graph_spectrum(raw_data, data, num_acqs)
            self.update_spectrum.clear()
            self.spectrum_updated.set()

def run():
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.title("Mass Spec Automator")
    root.style = ttkthemes.ThemedStyle()
    #print(ttkthemes.ThemedStyle().theme_names())
    root.style.theme_use("clearlooks")
    DisplayController(root)
    root.mainloop()

run()