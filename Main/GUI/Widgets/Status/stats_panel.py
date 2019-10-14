import tkinter as tk
from tkinter import ttk
import Main.GUI.Tools.display_tools as tools
from Main.Data import stats_info
from Main.Data.structs import Stat
import Main.Data.stats_info as stats

class StatsPanel:
    def __init__(self, win, side=tk.LEFT):
        self.all_stats = {}
        self.frame = ttk.LabelFrame(win, text="Status Bar")
        tools.create_blank_rows(self.frame, 2)
        self.pump_display = StatsFrame(win, self.frame, stats.PUMP_FRAME_LABEL, stats.PUMP_STAT_COLUMNS, stats.PUMP_INFO)
        self.all_stats = {**self.all_stats, **self.pump_display.stat_map}
        tools.create_blank_rows(self.frame, 2)
        self.voltage_display = StatsFrame(win, self.frame, stats.VOLTAGE_FRAME_LABEL, stats.VOLTAGE_STAT_COLUMNS, stats.VOLTAGE_INFO)
        self.all_stats = {**self.all_stats, **self.voltage_display.stat_map}
        tools.create_blank_rows(self.frame, 2)
        self.frame.pack(side=side, expand=tk.YES, fill=tk.BOTH)
        self.stat_frames = (self.voltage_display, self.pump_display)

    def disable(self):
        for frame in self.stat_frames:
            entries = frame.entries
            for key in entries.keys():
                entry = frame.entries[key]
                entry.configure(state="disabled")

    def enable(self):
        for frame in self.stat_frames:
            for key in frame.entries.keys():
                entry = frame.entries[key]
                entry.configure(state="normal")

    def pack(self, side):
        self.frame.pack(side=side)

class StatsFrame:
        def __init__(self, win, outer_frame, frame_label, num_columns, range_info, side=tk.TOP):
            self.win = win
            self.outer_frame = outer_frame
            self.num_columns = num_columns
            self.range_info = range_info
            self.field_names = list(self.range_info.keys())
            self.frame = ttk.Labelframe(outer_frame, text=frame_label)
            self.frame.pack(side=side)
            self.entries = tools.initialize_labeled_entry_display(frame=self.frame, labels=self.field_names,
                                                             cols=self.num_columns)
            self.stat_map = {}
            for name in self.entries.keys():
                range_set = self.range_info[name]
                stat = Stat(range_set)
                self.stat_map[name] = stat

        def reset(self):
            for key in self.entries.keys():
                entry = self.entries[key]
                entry.delete(0, tk.END)

        def display_stats(self, values):
            for key in values.keys():
                value = values[key]
                entry = self.entries[key]
                entry.delete(0, tk.END)
                entry.insert(0, value)
                stat = stats_info.ALL_INFO[key]
                color = stat.get_display_color(value=value)
                entry.configure(bg=color)