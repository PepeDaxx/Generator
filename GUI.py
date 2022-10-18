from tkinter import *
from tkinter import ttk

import tkcalendar
from tkcalendar import DateEntry


class GUI():
    def __init__(self):
        pass

    def create_frame(self, master):
        frame = ttk.Frame(master=master, padding=10, width=800, height=300)
        frame.pack()
        return frame

    def create_label(self, master, text=None):
        label = ttk.Label(master=master, text=text)
        label.pack()
        return label

    def create_button(self, master, command, text=None, side=None, ):
        button = ttk.Button(master=master, text=text, command=command)
        button.pack(side=side)
        return button

    def create_table(self, columns, master=None, side=None, ):
        self.table = ttk.Treeview(master, columns=columns, show='headings')
        self.table.bind('<Button-1>', lambda e: self.table_selection(self.table.identify_row(e.y)))
        for x in columns:
            self.table.column(f'{x}', width=len(x) * 30)
            self.table.heading(x, text=x, command=lambda c=x: self.sort_table(c, False))
        self.table.pack(side=side)
        scrollbar = ttk.Scrollbar(master, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='left', fill=Y)
        return self.table

    def sort_table(self, column, reverse):
        l = [(self.table.set(k, column), k) for k in self.table.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.table.move(k, '', index)
        self.table.heading(column, text=column, command=lambda _col=column: self.sort_table(_col, not reverse))

    def load_fixtures_into_table(self, content, table):
        table.delete(*table.get_children())
        for c in content:
            table.insert('', 'end', values=[c] + content[c])
        return self.table

    def update_predictions(self, id, match_id, preds, table):
        table.item(id, values=(table.item(id)["values"] + preds[match_id]))

    def create_date_entry(self, master):
        entry = tkcalendar.DateEntry(master)
        entry.pack()
        return entry

    def table_selection(self, event):
        self.selected_row = event

    def get_selection(self):
        return self.selected_row

    def table_menu(self, event):
        row = self.table.identify_row(event.y)
        self.table.selection_set(row)
        self.popup()

    def popup(self):
        self.popup_menu = Menu(self.root, tearoff=0)
