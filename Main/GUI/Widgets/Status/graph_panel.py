import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Main.GUI.Tools import plotter


class GraphPanel:

    def __init__(self, root, bottom_frame):
        self.root = root
        self.frame = ttk.LabelFrame(bottom_frame, text="Spectrum")
        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.pack()
        self.frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.canvas, self.axis = plotter.make_empty_graph(self.frame)

    def pack(self, side=tk.LEFT, expand=tk.YES, fill=tk.BOTH):
        self.frame.pack(side=side, expand=expand, fill=fill)

    def graph_spectrum(self, raw_data, data, num_acqs):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        plotter.display_graphs(data=data, raw_data=raw_data, num_acqs=num_acqs)
        #plotter.update_embedded_graph(self.canvas, axis=self.axis, data=data, raw_data=raw_data, num_acqs=num_acqs)

        '''
        The above commented line, which is used to update the embedded spectrum graph, crashes the program. 
        This will need to be debugged by someone who understands threading better than I do. For some reason, the 
        embedded matplotlib canvas cannot be dynamically updated.
        '''