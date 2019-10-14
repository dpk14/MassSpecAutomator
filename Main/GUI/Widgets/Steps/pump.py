from Main.BackEnd.msp430.Functions.Commands.ActivateRoughing import ActivateRoughing
from Main.BackEnd.msp430.Functions.Commands.ActivateTurbo import ActivateTurbo
from Main.BackEnd.msp430.Functions.Commands.DeactivateRoughing import DeactivateRoughing
from Main.BackEnd.msp430.Functions.Commands.DeactivateTurbo import DeactivateTurbo
import tkinter as tk
from tkinter import ttk

from Main.BackEnd.msp430.Functions.Queries.TurboOn import TurboOn
from Main.BackEnd.msp430.Functions.Queries.RoughingOn import RoughingOn
from Main.GUI.Tools import display_tools
from Main.GUI.Widgets.Steps.Step import Step


class PumpControl(Step):
    FRAME_LABEL = "Step 2: Pump Control"
    PUMP_BUTTON_LABELS = ["Turn Roughing Pump ", "Turn Turbo Pump "]
    ON_COMMANDS = {
                    PUMP_BUTTON_LABELS[0]: ActivateRoughing(),
                    PUMP_BUTTON_LABELS[1]: ActivateTurbo()
                    }
    OFF_COMMANDS = {
        PUMP_BUTTON_LABELS[0]: DeactivateRoughing(),
        PUMP_BUTTON_LABELS[1]: DeactivateTurbo()
    }
    NUM_COLUMNS = 2

    def __init__(self, win, outer_frame, communicator, console):
        self.win = win
        self.communicator = communicator
        self.outer_frame = outer_frame
        self.frame = ttk.Labelframe(outer_frame, text=self.FRAME_LABEL)
        self.frame.pack(side=tk.LEFT)
        self.buttons={}
        self.initialize_buttons()
        self.console = console
        super().__init__(self.frame)

    def reset(self):
        for i in range(len(self.entries)):
            self.entries[i].set("")

    def initialize_buttons(self):
        display_tools.create_blank_rows(self.frame)
        for label in self.PUMP_BUTTON_LABELS:
            button = tk.Button(self.frame, text=label + "ON", state=tk.DISABLED, bg='red')
            button['command'] = lambda lab=label: self.change_state(lab)
            self.buttons[label] = button
            button.pack(side=tk.TOP)

    def change_state(self, label, already_activated=False):
        button=self.buttons[label]
        if button['text'] == label + "ON":
            string_state = "OFF"
            button.configure(bg='green')
            if not already_activated:
                self.communicator.execute(command=self.ON_COMMANDS[label])
                self.console.display_command(self.ON_COMMANDS[label])
        else:
            self.communicator.execute(command=self.OFF_COMMANDS[label])
            self.console.display_command(self.OFF_COMMANDS[label])
            string_state = "ON"
            button.configure(bg='red')
        button.configure(text=label + string_state)

    def activate(self):
        for key in self.buttons.keys():
            button = self.buttons[key]
            button.configure(state=tk.NORMAL)
        query = RoughingOn()
        roughing_on = self.communicator.query(query)
        if roughing_on:
            self.change_state(self.PUMP_BUTTON_LABELS[0])
        query = TurboOn()
        turbo_on = self.communicator.query(query)
        if turbo_on:
            self.change_state(self.PUMP_BUTTON_LABELS[1])
