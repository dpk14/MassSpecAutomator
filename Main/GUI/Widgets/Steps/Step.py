import tkinter as tk

class Step:

    def __init__(self, frame):
        self.frame = frame

    def pack(self):
        self.frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def activate(self):
        pass

    def deactivate(self):
        pass