import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

curdir = os.path.abspath(os.path.dirname(__file__)) # Текущий каталог, где лежит программа

class MainTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # --- Элементы Tk ---
        self.label = tk.Label(self, text='Выберите файл csv с данными Wheellog')
        self.label.pack(padx=10, pady=10)
        
        self.button = ttk.Button(self, text = "Browse A File",command = self.fileDialog)
        self.button.pack()

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir =  curdir, title = "Select A File", filetypes = (("csv files","*.csv"),("All files","*.*")) )
        self.label.configure(text = self.filename)


if __name__ == '__main__':
    app = MainTk()
    app.mainloop()