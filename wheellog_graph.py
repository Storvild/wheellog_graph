import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import matplotlib
import matplotlib.pyplot
from tk_zoom import ZoomPan


curdir = os.path.abspath(os.path.dirname(__file__)) # Текущий каталог, где лежит программа


def get_data(filename):
    """ Тестовые данные """ 
    from datetime import datetime
    xdata = [datetime(2020, 5, 28, 7, 52, 1, 523000), datetime(2020, 5, 28, 7, 52, 2, 566000), datetime(2020, 5, 28, 7, 52, 2, 725000), datetime(2020, 5, 28, 7, 52, 2, 923000), datetime(2020, 5, 28, 7, 52, 3, 114000), datetime(2020, 5, 28, 7, 52, 3, 309000)]
    ydata = [1.26, 3.52, 11.85, 18.56, 4.27, 10.9]
    ypower_data = [0.0067, 0.7329000000000001, 4.3957, 3.6575, -0.8995000000000001, 5.0323]
    return (xdata, ydata, ypower_data)


class MainTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # --- Элементы Tk ---
        self.label = tk.Label(self, text='Выберите файл csv с данными Wheellog')
        self.label.pack(padx=10, pady=10)
        
        self.button = ttk.Button(self, text = "Browse A File",command = self.fileDialog)
        self.button.pack()
        
        self.graph_draw('')
        
        # --- Выход из программы ---
        self.bind('<Button-2>', lambda event: exit()) # Выход по средней кнопки мыши
        self.bind('<Escape>', lambda event: exit())   # Выход по Esc
        # --------------------------
        
    def format_coord(self, x, y):
        timeformat = matplotlib.dates.num2date(x).strftime('%H:%M:%S')
        return 'Время: {} Скорость: {} км/ч Мощность: {} Вт'.format(timeformat, round(y,1), round(y*100,0))

    def graph_draw(self, filename):
        # --- График ---
        fig, ax = matplotlib.pyplot.subplots() # Создание фигуры fig и осей ax (axes)
        
        xdata, ydata, ypower_data = get_data('') # Данные для построения графика
        ax.plot(xdata, ydata, color="green", label="Скорость")
        ax.plot(xdata, ypower_data, color="red", label="Мощность Y*100")
        fig.autofmt_xdate() # Наклонные надписи на оси X
        ax.set_xlabel('Время') # Подписать ось X
        ax.set_ylabel('Y') # Подписать ось Y
        ax.legend() # Показать легенду
        ax.grid() # Показать сетку
        ax.format_coord = self.format_coord # Показ координат не как x, y, а как Время, Скорость, Мощность

        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, self)
        #self.canvas.draw() 
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)    
        
        # --- Масштабирование графика ---
        zp = ZoomPan()
        zp.apply(ax, base_scale=1.3)

        # --- Тулбар ---
        self.toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()


    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir =  curdir, title = "Select A File", filetypes = (("csv files","*.csv"),("All files","*.*")) )
        self.label.configure(text = self.filename)


if __name__ == '__main__':
    app = MainTk()
    app.mainloop()