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


def get_wheellog_data(filename):
    import csv
    from datetime import datetime as dt
    #if not filename:
    #    filename = r'e:\NEW\2020-03-10\matplotlib\wheellog\2020_05_28_07_52_00.csv'
    data = []
    with open(filename,'r') as f:
        rdr = csv.DictReader(f)
        lspeed_avg = 0
        for i, x in enumerate(rdr):
            lspeed_avg = float(x['speed'])
            lpower = float(x['power'])
            data.append({'datetime':dt.strptime(x['date']+' '+x['time'],'%Y-%m-%d %H:%M:%S.%f'), 'speed':lspeed_avg, 'power':lpower})
    xdata = [x['datetime'] for x in data] #[:100]
    ydata = [x['speed'] for x in data] #[:100]
    ypower_data = [x['power']/100 for x in data] 
    return (xdata, ydata, ypower_data)


class MainTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # --- Элементы Tk ---
        self.label = tk.Label(self, text='Выберите файл csv с данными Wheellog')
        self.label.pack(padx=10, pady=10)
        
        self.button = ttk.Button(self, text = "Browse A File",command = self.fileDialog)
        self.button.pack()
       
        # --- Фрейм на котором будет график (нужен, чтобы график потом уничтожить вместе с фреймом для загрузки нового)
        self.graphframe = tk.Frame()
        self.graphframe.pack(expand=1, fill='both')
        
        # --- Фрейм на котором будет тулбар
        self.toolbarframe = tk.Frame()
        self.toolbarframe.pack(expand=1, fill='both')
        
        filename = ''
        self.graph_draw(filename)
        
        # --- Выход из программы (вынесено в ZoomPan) ---
        #self.bind('<Button-2>', lambda event: self.destroy()) # Выход по средней кнопки мыши
        #self.bind('<Escape>', lambda event: self.destroy())   # Выход по Esc
        # --------------------------
    
    def format_coord(self, x, y):
        timeformat = matplotlib.dates.num2date(x).strftime('%H:%M:%S')
        return 'Время: {} Скорость: {} км/ч Мощность: {} Вт'.format(timeformat, round(y,1), round(y*100,0))
    
    def graph_draw(self, filename):
        # Создаем фигуру fig и оси ax
        fig, ax = matplotlib.pyplot.subplots()
        
        if filename:
            xdata, ydata, ypower_data = get_wheellog_data(filename) # Данные для построения графика
            #xdata, ydata, ypower_data = get_data(filename) # Данные для построения графика
            ax.plot(xdata, ydata, color="green", label="Скорость")
            ax.plot(xdata, ypower_data, color="red", label="Мощность Y*100")
        fig.autofmt_xdate() # Наклонные надписи на оси X
        ax.set_xlabel('Время') # Подписать ось X
        ax.set_ylabel('Y') # Подписать ось Y
        ax.legend() # Показать легенду
        ax.grid() # Показать сетку
        ax.format_coord = self.format_coord # Показ координат не как x, y, а как Время, Скорость, Мощность

        # --- Отрисовка ---
        self.graphframe.destroy()
        self.graphframe = tk.Frame()
        self.graphframe.pack(expand=1, fill='both')

        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, self.graphframe) # Было (fig, self)
        #self.canvas.draw() 
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)    
    
        # --- Масштабирование графика ---
        zp = ZoomPan()
        zp.apply(ax, base_scale=1.3)

        # --- Тулбар ---
        self.toolbarframe.destroy()
        self.toolbarframe = tk.Frame()
        self.toolbarframe.pack(expand=1, fill='both')
        
        self.toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2Tk(self.canvas, self.toolbarframe)
        self.toolbar.update()
    
        self.label.configure(text = filename)
    
    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir =  curdir, title = "Select A File", filetypes = (("csv files","*.csv"),("All files","*.*")) )
        self.graph_draw(self.filename)
        

if __name__ == '__main__':
    app = MainTk()
    app.mainloop()