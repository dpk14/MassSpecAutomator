import threading
import time
from Main.BackEnd.msp430.Functions.Commands.AdjustPWMVoltage import AdjustPWMVoltage

import tkinter as tk
from tkinter import ttk

from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Functions.Queries.FanOn import FanOn
from Main.BackEnd.msp430.Functions.Queries.TEOn import TEOn
from Main.BackEnd.msp430.Library import commands
from Main.GUI.Widgets.Steps.Step import Step
from Main.GUI.Tools import defaults, display_tools


class ThermalElectricDisplay(Step):
    TE_FAN_LABEL = "Turn Fan "
    TE_LABEL = "Turn Thermal Electric "
    TURN_FAN_ON = TE_FAN_LABEL + "ON"
    TURN_FAN_OFF = TE_FAN_LABEL + "OFF"
    TURN_TE_ON = TE_LABEL + "ON"
    TURN_TE_OFF = TE_LABEL + "OFF"

    PWM_LABEL= "Set TE PWM"
    FRAME_LABEL = "Step 4: Thermal Electric"

    def __init__(self, win, outer_frame, communicator, console):
        self.win = win
        self.communicator = communicator
        self.outer_frame = outer_frame
        self.frame = ttk.Labelframe(outer_frame, text=self.FRAME_LABEL)
        self.PWM_percent = 0
        self.console = console
        self.initialize_TE_interface()
        super().__init__(self.frame)

    def initialize_TE_interface(self):
        display_tools.create_blank_rows(self.frame)
        self.therm_fan_button = ttk.Button(self.frame, text=self.TURN_FAN_ON, state=tk.DISABLED)
        self.therm_fan_button['command'] = lambda already_activated=False: self.change_fan(already_activated=already_activated)
        self.therm_fan_button.pack(side=tk.TOP)
        self.therm_electric_button = ttk.Button(self.frame, text=self.TURN_TE_ON, state=tk.DISABLED)
        self.therm_electric_button['command'] = lambda already_activated=False: self.change_te(already_activated)
        self.therm_electric_button.pack(side=tk.TOP)
        self.make_PWM_regulator()

    def change_fan(self, already_activated):
        if self.therm_fan_button["text"] == self.TURN_FAN_ON:
            self.therm_fan_button.configure(text=self.TURN_FAN_OFF)
            self.therm_electric_button.configure(state=tk.NORMAL)
            if not already_activated:
                command = Command(commands.THERM_ELEC_FAN_ON)
                self.communicator.execute(command=command)
                self.console.display_command(command)
        else:
            self.therm_fan_button.configure(text=self.TURN_FAN_ON)
            self.therm_electric_button.configure(state=tk.DISABLED)
            command = Command(commands.THERM_ELEC_FAN_OFF)
            self.communicator.execute(command=command)
            self.console.display_command(command)

    def change_te(self, already_activated):
        if self.therm_electric_button["text"] == self.TURN_TE_ON:
            self.therm_electric_button.configure(text=self.TURN_TE_OFF)
            self.therm_fan_button.configure(state=tk.DISABLED)
            self.regulator_button.configure(state=tk.NORMAL)
            if not already_activated:
                command = Command(commands.THERM_ELEC_V_ON)
                self.communicator.execute(command=command)
                self.console.display_command(command)
        else:
            self.therm_electric_button.configure(text=self.TURN_TE_ON)
            self.therm_fan_button.configure(state=tk.NORMAL)
            self.regulator_button.configure(state=tk.DISABLED)
            command = Command(commands.THERM_ELEC_V_OFF)
            self.communicator.execute(command=command)
            self.console.display_command(command)

    def make_PWM_regulator(self):
        self.regulator_button = ttk.Button(self.frame, text=self.PWM_LABEL)
        self.regulator_button.pack(side=tk.LEFT)
        self.TE_percentage = tk.StringVar()
        choices=[]
        for percentage in range(defaults.MAX_TM_PERCENTAGE):
            if percentage % defaults.TM_STEP == 0:
                choices.append(str(percentage))
        self.TE_percentage.set('00')  # set the default option
        self.popupMenu = ttk.Combobox(self.frame, text="TE:", state=tk.DISABLED, values=choices)
        self.popupMenu.pack(side=tk.LEFT)
        self.popupMenu.configure(textvariable=self.TE_percentage)
        self.regulator_button['command'] = lambda end=self.TE_percentage: self.step_thread(end)
        self.regulator_button.configure(state="disabled")

    def step_thread(self, end):
        x = threading.Thread(target=self.step_therm_elec, args=(end, ))
        x.start()

    def step_therm_elec(self, end):
        self.regulator_button.configure(text="Stepping...")
        self.regulator_button.configure(state="disabled")
        end = float("." + end.get()[0])
        print(end)
        while self.PWM_percent < end:
            self.PWM_percent += .1
            print(self.PWM_percent, end)
            self.adjust_voltage(self.PWM_percent, end)
        while int(self.PWM_percent) > end:
            self.PWM_percent -= .1
            self.adjust_voltage(self.PWM_percent, end)
        self.regulator_button.configure(state="normal")
        self.regulator_button.configure(text=self.PWM_LABEL)

    def adjust_voltage(self, PWM_percent, end):
        tenths_place = str(PWM_percent)[2]
        func = AdjustPWMVoltage(percent=tenths_place)
        self.communicator.execute(func)
        self.console.display_command(func)
        message = "Thermal Electric is at " + tenths_place + "0% of maximum voltage"
        self.console.display(message)
        if PWM_percent == end:
            return
        time.sleep(defaults.THERM_STEP_DELAY)

    def activate(self):
        self.popupMenu.configure(state=tk.NORMAL)
        self.therm_fan_button.configure(state=tk.NORMAL)
        query = FanOn()
        fan_on = self.communicator.query(query)
        query = TEOn()
        te_on = self.communicator.query(query)
        if fan_on:
            self.change_fan(already_activated=True)
        if te_on:
            self.change_fan(already_activated=True)
            self.change_te(already_activated=True)