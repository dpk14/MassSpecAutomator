import threading

from Main.BackEnd.msp430.Functions.Commands.ActivateElectricSector import ActivateElectricSector
from Main.BackEnd.msp430.Functions.Commands.DeactivateElectricSector import DeactivateElectricSector
import tkinter as tk
from tkinter import ttk

from Main.BackEnd.msp430.Functions.Queries.ElecSecOn import ElecSecOn
from Main.BackEnd.msp430.Library import commands
from Main.GUI.Widgets.Steps.Step import Step
from Main.GUI.Tools import display_tools


class ElectricSectorDisplay(Step):
    GPIB_DEVICE = "Keithley"

    ESP_TITLE = "Electric Sector Positive"
    ESN_TITLE = "Electric Sector Negative"
    SECTORS = [ESP_TITLE, ESN_TITLE]

    POWER_LABEL = "Power Sectors "
    TURN_ON = POWER_LABEL + "ON"
    TURN_OFF = POWER_LABEL + "OFF"

    CALIBRATION_COMPLETE = {
        ESP_TITLE: False,
        ESN_TITLE: False
    }

    def __init__(self, win, outer_frame, communicator, console):
        self.frame = ttk.LabelFrame(outer_frame, text="Step 3: Electric Sector")
        self.stats = {}
        self.communicator = communicator
        self.console = console
        self.fill_interface()
        super().__init__(self.frame)

    def fill_interface(self):
        display_tools.create_blank_rows(self.frame)
        self.config_button = ttk.Button(self.frame, text=self.TURN_ON, state=tk.DISABLED, command=self.change_state)
        self.config_button.pack()
        display_tools.create_blank_rows(self.frame)
        self.make_sector_frames()

    def make_sector_frames(self):
        self.entry_map = {}
        self.buttons = {}
        self.gpib_id_map = {}
        self.button_frames = {}
        self.checkmarks = {}

        for sector in self.SECTORS:
            sector_frame = ttk.LabelFrame(self.frame, text=sector)
            sector_frame.pack(side=tk.TOP)

            voltage_frame = ttk.Frame(sector_frame)
            voltage_frame.pack(side=tk.TOP)
            display_tools.create_blank_rows(voltage_frame)
            voltage_label = ttk.Label(voltage_frame, text="Desired Voltage:")
            voltage_label.pack(side=tk.LEFT)
            voltage_entry = ttk.Entry(voltage_frame, state="disabled")
            voltage_entry.pack(side=tk.LEFT)
            self.entry_map[sector] = voltage_entry

            id_frame = ttk.Frame(sector_frame)
            id_frame.pack(side=tk.TOP)

            display_tools.create_blank_rows(id_frame)
            id_label = ttk.Label(voltage_frame, text="GPIB Device ID:")
            id_label.pack(side=tk.LEFT)
            id_entry = ttk.Entry(voltage_frame, state="disabled")
            id_entry.pack(side=tk.LEFT)
            self.gpib_id_map[sector] = id_entry

            button_frame = ttk.Frame(sector_frame)
            button_frame.pack(side=tk.TOP)
            button = ttk.Button(button_frame, text="Enter", state="disabled", command=lambda sec=sector: self.run(sec))
            button.pack(side=tk.LEFT, anchor=tk.CENTER)
            self.buttons[sector] = button
            self.button_frames[sector] = button_frame

            display_tools.create_blank_rows(self.frame)

    def change_state(self, already_activated=False):
        if self.config_button['text'] == self.TURN_ON:
            self.config_button.configure(text=self.TURN_OFF)
            for sector in self.SECTORS:
                self.entry_map[sector].configure(state="normal")
                self.gpib_id_map[sector].configure(state="normal")
            for key in self.buttons.keys():
                button = self.buttons[key]
                button.configure(state="normal")
            if not already_activated:
                command = ActivateElectricSector()
                self.communicator.execute(command=command)
                self.console.display_command(command)
        else:
            self.config_button.configure(text=self.TURN_ON)
            for sector in self.SECTORS:
                self.entry_map[sector].configure(state="disabled")
                self.gpib_id_map[sector].configure(state="disabled")
            for key in self.buttons.keys():
                button = self.buttons[key]
                button.configure(state="disabled")
            for key in self.checkmarks.keys():
                self.checkmarks[key] = ""
            command = DeactivateElectricSector()
            self.communicator.execute(command=command)
            self.console.display_command(command)

    def run(self, sector):
        calibration_thread = threading.Thread(target=self.calibrate_sector, args=(sector,))
        calibration_thread.start()

    def calibrate_sector(self, sector):
        desired_voltage = self.entry_map[sector].get()
        gpib_id = self.gpib_id_map[sector].get()
        error_message = self.validate_inputs(desired_voltage, gpib_id)
        if len(error_message) > 0:
            display_tools.display_error_box(error_message)
            return
        desired_voltage = float(desired_voltage)
        gpib_id = int(desired_voltage)
        '''
        device = GPIB_Device(device_type=GPIB_DEVICE, id=gpib_id)
        function = SrcVoltsGetCurrent(voltage=desired_voltage)
        device.execute(function)
        '''
        if not self.CALIBRATION_COMPLETE[sector]:
            checkmark_frame = self.button_frames[sector]
            checkmark = ttk.Label(checkmark_frame, text=display_tools.CHECKMARK)
            checkmark.pack(side=tk.LEFT)
            self.checkmarks[sector] = checkmark
        self.CALIBRATION_COMPLETE[sector] = True
        for key in self.CALIBRATION_COMPLETE.keys():
            if not self.CALIBRATION_COMPLETE[key]:
                return

    def validate_inputs(self, desired_voltage, gpib_id):
        if len(desired_voltage) == 0:
            return "No voltage entered"
        if len(gpib_id) == 0:
            return "No ID entered"
        try:
            int(gpib_id)
        except:
            return "ID must be an integer"
        try:
            int(desired_voltage)
        except:
            return "Invalid voltage syntax"
        return ""

    def activate(self):
        query = ElecSecOn()
        elec_sec_on = self.communicator.query(query)
        self.config_button.configure(state=tk.NORMAL)
        if elec_sec_on:
            self.change_state(execute_command=False)
