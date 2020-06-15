import tkinter as tk
from tkinter import ttk


class MainTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


if __name__ == '__main__':
    app = MainTk()
    app.mainloop()