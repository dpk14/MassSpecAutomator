import threading
import time

from Main.Controller import communication_controller
from Main.Visual_Interface.Steps.step import Step
import Main.Data.stats_info as info
from Main.Visual_Interface.Tools.structs import Stat
import tkinter as tk
from tkinter import ttk
import Main.Visual_Interface.Tools.display_toolkit as tools
import Main.BackEnd.msp430.Library.commands as commands

ESP_TITLE = "Electric Sector Positive"
ESN_TITLE = "Electric Sector Negative"
SECTORS = [ESP_TITLE, ESN_TITLE]

CALIBRATION_COMPLETE = {
                ESP_TITLE: False,
                ESN_TITLE: False
                }

LITTLE_STEP = 1
MEDIUM_STEP = 10
BIG_STEP = 100

VOLTAGE_STEPS = [BIG_STEP, MEDIUM_STEP, LITTLE_STEP]

ESP_LIBRARY = {
                    -LITTLE_STEP : commands.ELEC_SEC_POS_DOWN_1,
                    -MEDIUM_STEP : commands.ELEC_SEC_POS_DOWN_10,
                    -BIG_STEP : commands.ELEC_SEC_POS_DOWN_100,
                    LITTLE_STEP : commands.ELEC_SEC_POS_UP_1,
                    MEDIUM_STEP : commands.ELEC_SEC_POS_UP_10,
                    BIG_STEP: commands.ELEC_SEC_POS_UP_100,
                    }

ESN_LIBRARY =   {
                    -LITTLE_STEP : commands.ELEC_SEC_NEG_DOWN_1,
                    -MEDIUM_STEP : commands.ELEC_SEC_NEG_DOWN_10,
                    -BIG_STEP : commands.ELEC_SEC_NEG_DOWN_100,
                    LITTLE_STEP : commands.ELEC_SEC_NEG_UP_1,
                    MEDIUM_STEP : commands.ELEC_SEC_NEG_UP_10,
                    BIG_STEP : commands.ELEC_SEC_NEG_UP_100,
                    }

CONSOLE_LIBRARY = {
                    ESP_TITLE: ESP_LIBRARY,
                    ESN_TITLE: ESN_LIBRARY
                    }


class ElecSecStep(Step):

    FIELDS_NEEDED = ()

    def __init__(self, name, tab, notebook, index, all_stats, communicator, next_step=None):
        super().__init__(name, tab, notebook, index, all_stats, communicator, self.FIELDS_NEEDED, next_step)

    def fill_interface(self):
        tools.create_blank_rows(self.frame, 2)
        button = ttk.Button(self.frame, text="Power Sectors On", command= self.start_step)
        button.pack()
        self.entry_map = {}
        self.console_map = {}
        self.buttons = []
        for sector in SECTORS:
            frame = ttk.LabelFrame(self.frame, text=sector)
            frame.pack(side=tk.TOP)
            button = ttk.Button(frame, text="Enter", state="disabled", command= lambda sec = sector: self.run(sec))
            button.pack(side=tk.LEFT)
            self.buttons.append(button)

            entry = tk.Entry(frame, state="disabled")
            entry.pack(side=tk.LEFT)
            current_stat = Stat(entry, range_set=info.ELEC_SEC_INFO[sector])
            self.entry_map[sector] = current_stat

            listboxes = tools.make_scrollable_listboxes(frame, labels=("Console", ), width=30, height=10, side=tk.BOTTOM)
            console = listboxes[0]
            self.console_map[sector] = console
            button = ttk.Button(frame, text="Reset",  state="disabled", command=console.delete(0, tk.END))
            button.pack()
            self.buttons.append(button)

    def start_step(self):
        for sector in SECTORS:
            self.entry_map[sector].entry.configure(state="normal")
        for button in self.buttons:
            button.configure(state="normal")
        self.communicator.send_string(commands.ELEC_SEC_ON)

    def run(self, sector):
        calibration_thread = threading.Thread(target=self.calibrate_sector, args=(sector,))
        calibration_thread.start()

    def calibrate_sector(self, sector):

        desired_stat = self.entry_map[sector]
        desired_val = desired_stat.entry.get()
        console = self.console_map[sector]
        console_commands = CONSOLE_LIBRARY[sector]
        val = -1
        while True:
            if desired_stat.in_range(desired_stat.good, val):
                break

            values = communication_controller.generate_test_stats()
            val = values[sector]
            console.insert(tk.END, "Voltage is now " + val + " Volts")
            sign = 1
            if val > desired_val:
                sign = -1
            for step in VOLTAGE_STEPS:
                if val + step * sign < desired_val:
                    self.communicator.send_string(console_commands[step * sign])
                    break
            time.sleep(communication_controller.SYSTEM_DELAY*5)
        console.insert(tk.END, "Calibration Complete!")
        CALIBRATION_COMPLETE[sector] = True
        for key in CALIBRATION_COMPLETE.keys():
            if not CALIBRATION_COMPLETE[key]:
                return
        self.step_complete()