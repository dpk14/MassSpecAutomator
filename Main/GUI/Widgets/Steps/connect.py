from tkinter import ttk
import tkinter as tk

from Main.BackEnd.msp430.Functions.Queries.Interrogate import Interrogate
from Main.GUI.Tools import display_tools
from Main.GUI.Widgets.Steps.Step import Step

NOT_CONNECTED_ERROR = "msp430 not connected!"

class ConnectDisplay(Step):

    def __init__(self, win, outer_frame, communicator, console):
        self.win = win
        self.outer_frame = outer_frame
        self.communicator = communicator
        self.frame = ttk.LabelFrame(outer_frame, text="Step 1: Connect")
        display_tools.create_blank_rows(self.frame)
        super().__init__(self.frame)


    def make_connect_button(self, connection_event):
        self.connection_event = connection_event
        self.connect_button = ttk.Button(self.frame, text="Connect")
        self.connect_button['command'] = lambda: self.change_connection()
        self.connect_button.pack(anchor=tk.CENTER)
        return self.connect_button

    def change_connection(self):
        if self.connect_button['text'] == "Connect":
            try:
                self.communicator.connect()
            except:
                display_tools.display_error_box(NOT_CONNECTED_ERROR)
                return
            self.connect_button['text'] = "Disconnect"
            self.connection_event.set()
        else:
            self.connect_button['text'] = "Connect"
            self.connection_event.set()

    def reset_connect_button(self):
        self.connect_button.configure(text="Connect")
