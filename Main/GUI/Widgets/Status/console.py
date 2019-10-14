import tkinter as tk
from tkinter import ttk

from Main.BackEnd.msp430.Functions.Commands.Command import Command
from Main.BackEnd.msp430.Functions.Queries.Interrogate import Interrogate
from Main.BackEnd.msp430.Functions.Queries.Query import Query
from Main.BackEnd.msp430.Library import commands
from Main.GUI.Tools import display_tools, defaults


class Console:
    BUTTON_LABEL = "SEND"
    OUTPUT_HEADER = ">> "

    def __init__(self, outer_frame, communicator):
        self.outer_frame = outer_frame
        self.communicator = communicator
        self.frame = ttk.LabelFrame(self.outer_frame, text="Console")
        self.frame.pack(side=tk.BOTTOM)
        send_box_frame = ttk.Frame(self.frame)
        send_box_frame.pack(side=tk.TOP)
        display_tools.create_blank_rows(self.frame)
        console_frame = ttk.Frame(self.frame)
        console_frame.pack(side=tk.TOP)
        display_tools.create_blank_rows(send_box_frame)
        self.entry = display_tools.create_packed_entry_box(frame=send_box_frame, side=tk.LEFT)
        self.send_button = ttk.Button(send_box_frame, text="SEND", state=tk.DISABLED)
        self.send_button['command'] = self.display_entry
        self.send_button.pack(side=tk.LEFT)
        self.listbox = display_tools.make_scrollable_listbox(frame=console_frame,
                                                   height=defaults.CONSOLE_LISTBOX_HEIGHT, width=defaults.CONSOLE_LISTBOX_WIDTH, side=tk.TOP)

    def pack(self, side):
        self.frame.pack(side=side, expand=tk.YES, fill=tk.BOTH)

    def display_entry(self):
        entry = self.entry.get()
        command = Command(entry)
        self.display_command(command=command)

    def display_command(self, command):
        message = command.executable
        for sub_message in message:
            if sub_message[0] is not ".":
                response = defaults.INVALID_SYNTAX_EXCEPTION
            else:
                try:
                    response = self.communicator.query(query=Query(sub_message))
                except:
                    try:
                        self.communicator.query(Interrogate())
                        response = defaults.INVALID_SYNTAX_EXCEPTION
                    except:
                        response = defaults.DISCONNECTED_EXCEPTION
            formatted_response = self.OUTPUT_HEADER + response
            self.display(sub_message)
            self.display(formatted_response)

    def display(self, message):
        self.listbox.insert(tk.END, message)

    def activate(self):
        self.send_button.configure(state="normal")

    def deactivate(self):
        self.send_button.configure(state="disabled")
