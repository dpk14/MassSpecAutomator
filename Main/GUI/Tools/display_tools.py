import tkinter as tk
from tkinter import ttk, messagebox

ENTRY_WIDTH = 12
CHECKMARK = u"\u2713"

def create_blank_rows(frame, num_rows=1):
    for k in range(num_rows):
        label = ttk.Label(frame, text="   ")
        label.pack(side=tk.TOP)

def create_blank_cols(frame, num_cols=1):
    for k in range(num_cols):
        label = ttk.Label(frame, text="")
        label.pack(side=tk.RIGHT)

def create_label(frame, text, column, row):
    label = ttk.Label(frame, text=text)
    label.grid(column=column, row=row)

def create_entry_box(win, frame, row, column, text=""):
    current_variable = tk.StringVar(frame, value=text)
    current_entry = ttk.Entry(frame, width=ENTRY_WIDTH, textvariable=current_variable)
    current_entry.grid(column=column, row=row)
    return current_entry

def create_packed_entry_box(frame, text="", read_only=False, side=tk.LEFT):
    current_variable = tk.StringVar(frame, value=text)
    current_entry = ttk.Entry(frame, width=ENTRY_WIDTH, textvariable=current_variable)
    if read_only:
        current_entry.configure(state='readonly')
    current_entry.pack(side=side)
    return current_entry

def create_check_box(self, text, row, column):
    current_variable = (tk.IntVar(),)
    checkbox = ttk.Checkbutton(self.frame, text=text, variable=current_variable)
    checkbox.grid(column=column, row=row)
    return current_variable

def initialize_labeled_entry_display(frame, labels, cols):
    entries = {}
    num_of_entries = len(labels)
    entries_per_col = int(round(num_of_entries)/cols)
    entries_in_last_col = num_of_entries - entries_per_col*(cols-1)
    for j in range(cols-1):
        for i in range(entries_per_col):
            row = i + entries_per_col*j
            label = labels[i]
            create_label(frame, text=label, column=j*2, row=row)
            entry = tk.Entry(frame)
            entry.grid(column=(j*2)+1, row=row)
            entries[label] = entry
    for i in range(entries_in_last_col):
        label = labels[num_of_entries-entries_in_last_col+i]
        create_label(frame, text=label, column=cols*2, row=i)
        entry = tk.Entry(frame)
        entry.grid(column=cols*2 + 1, row=i)
        entries[label] = entry
    return entries

def make_scrollable_listbox(frame, width, height, side=tk.TOP):
    scrollbar = ttk.Scrollbar(frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(frame, width=width, height=height, yscrollcommand=scrollbar.set)
    listbox.pack(side=side)
    scrollbar.config(command=listbox.yview)
    return listbox

def set_stat_field_color(stat):
    if stat.in_range(stat.good):
        stat.entry.configure(bg="green")
    elif stat.in_range(stat.passable):
        stat.entry.configure(bg="orange")
    else:
        stat.entry.configure(bg="red")

def step_completed(tab):
    return tab.step_enabled

def display_error_box(error_message):
    messagebox.showerror("Error", error_message)
