import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import matplotlib
import matplotlib.pyplot
from tk_zoom import ZoomPan

curdir = os.path.abspath(os.path.dirname(__file__))  # Текущий каталог, где лежит программа


def get_data(filename):
    """ Тестовые данные """
    from datetime import datetime
    xdata = [datetime(2020, 5, 28, 7, 52, 1, 523000), datetime(2020, 5, 28, 7, 52, 2, 566000),
             datetime(2020, 5, 28, 7, 52, 2, 725000), datetime(2020, 5, 28, 7, 52, 2, 923000),
             datetime(2020, 5, 28, 7, 52, 3, 114000), datetime(2020, 5, 28, 7, 52, 3, 309000)]
    ydata = [1.26, 3.52, 11.85, 18.56, 4.27, 10.9]
    ypower_data = [0.0067, 0.7329000000000001, 4.3957, 3.6575, -0.8995000000000001, 5.0323]
    return (xdata, ydata, ypower_data)


def get_wheellog_data(filename):
    import csv
    from datetime import datetime as dt
    # if not filename:
    #    filename = r'e:\NEW\2020-03-10\matplotlib\wheellog\2020_05_28_07_52_00.csv'
    data = []
    with open(filename, 'r') as f:
        rdr = csv.DictReader(f)
        lspeed_avg = 0
        for i, x in enumerate(rdr):
            lspeed_avg = float(x['speed'])
            lpower = float(x['power'])
            data.append(
                {'datetime': dt.strptime(x['date'] + ' ' + x['time'], '%Y-%m-%d %H:%M:%S.%f'), 'speed': lspeed_avg,
                 'power': lpower})
    xdata = [x['datetime'] for x in data]  # [:100]
    ydata = [x['speed'] for x in data]  # [:100]
    ypower_data = [x['power'] / 100 for x in data]
    return (xdata, ydata, ypower_data)


class MainTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # --- Элементы Tk ---
        self.label = tk.Label(self, text='Выберите файл csv с данными Wheellog')
        self.label.pack(padx=10, pady=10)

        self.button = ttk.Button(self, text="Browse A File", command=self.fileDialog)
        self.button.pack()

        self.label_info = tk.Label(self, text='', anchor='w', bg='yellow', font=("TkFixedFont", 10), justify='left')
        self.label_info.pack(padx=10, pady=10, fill='both')

        # --- Фрейм на котором будет график (нужен, чтобы график потом уничтожить вместе с фреймом для загрузки нового)
        self.graphframe = tk.Frame()
        self.graphframe.pack(expand=1, fill='both')

        # --- Фрейм на котором будет тулбар
        self.toolbarframe = tk.Frame()
        self.toolbarframe.pack(expand=1, fill='both')

        filename = ''
        self.graph_draw(filename)

        # --- Выход из программы (вынесено в ZoomPan) ---
        # self.bind('<Button-2>', lambda event: self.destroy()) # Выход по средней кнопки мыши
        # self.bind('<Escape>', lambda event: self.destroy())   # Выход по Esc
        # self.bind('<Escape>', lambda event: exit())   # Выход по Esc
        self.bind('<Escape>', self.myexit)  # Выход по Esc
        # --------------------------

    def myexit(self, event):
        # self.ax.clear()
        # self.ax.remove()
        # self.ax.axis("off")
        # self.destroy()
        exit()

    def format_coord(self, x, y):
        timeformat = matplotlib.dates.num2date(x).strftime('%H:%M:%S')

        # self.label_info.config(text='x={} y={}'.format(x, y))
        if hasattr(self, 'xdata'):
            for idx, a in enumerate(self.xdata):
                if matplotlib.dates.date2num(a) > x:
                    self.label_info.config(
                        text='Время:{} Скорость={:>6}км/ч Мощность={:>5}Вт x={:>19} y={:>19}'.format(
                                timeformat, round(self.ydata[idx], 1), round(self.ypower_data[idx] * 100), x, y))
                    if self.scatter1:
                        self.scatter1.remove()
                    if self.scatter2:
                        self.scatter2.remove()
                    self.scatter1 = self.ax.scatter([x], [self.ydata[idx]])
                    self.scatter2 = self.ax.scatter([x], [self.ypower_data[idx]])
                    self.canvas.draw()
                    break

        # self.ax.text(x, y, 'TEST')
        # self.ax.scatter([x], [y])
        return 'Время: {} Скорость: {} км/ч Мощность: {} Вт'.format(timeformat, round(y, 1), round(y * 100, 0))

    def on_mouse_move(self, event):
        if hasattr(self, 'xdata') and event.xdata and event.ydata:
        #if event.xdata:
            #print(event.xdata, event.ydata)
            timeformat = matplotlib.dates.num2date(event.xdata).strftime('%H:%M:%S')

            for idx, a in enumerate(self.xdata):
                if matplotlib.dates.date2num(a) > event.xdata:
                    self.label_info.config(
                        text='Время:{} Скорость={:>6}км/ч Мощность={:>5}Вт\nx={:>4} y={:>4}\nxdata={:>20} ydata={:>20}'.format(
                                timeformat, round(self.ydata[idx], 1), round(self.ypower_data[idx] * 100),
                                event.x, event.y,
                                event.xdata, event.ydata))
                    if self.scatter1:
                        self.scatter1.remove()
                    if self.scatter2:
                        self.scatter2.remove()
                    self.scatter1 = self.ax.scatter([self.xdata[idx]], [self.ydata[idx]])
                    self.scatter2 = self.ax.scatter([self.xdata[idx]], [self.ypower_data[idx]])
                    self.canvas.draw()
                    break


    def graph_draw(self, filename):
        # Создаем фигуру fig и оси ax
        self.fig, self.ax = matplotlib.pyplot.subplots()

        if filename:
            self.xdata, self.ydata, self.ypower_data = get_wheellog_data(filename)  # Данные для построения графика
            # xdata, ydata, ypower_data = get_data(filename) # Данные для построения графика
            self.ax.plot(self.xdata, self.ydata, color="green", label="Скорость")
            self.ax.plot(self.xdata, self.ypower_data, color="red", label="Мощность Y*100", linestyle='-')
        self.fig.autofmt_xdate()  # Наклонные надписи на оси X
        self.ax.set_xlabel('Время')  # Подписать ось X
        self.ax.set_ylabel('Y')  # Подписать ось Y
        # self.ax.legend() # Показать легенду
        self.ax.grid()  # Показать сетку
        self.ax.format_coord = self.format_coord  # Показ координат не как x, y, а как Время, Скорость, Мощность

        # --- Отрисовка ---
        self.graphframe.destroy()
        self.graphframe = tk.Frame()
        self.graphframe.pack(expand=1, fill='both')

        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, self.graphframe)  # Было (fig, self)
        # self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # --- Масштабирование графика ---
        zp = ZoomPan()
        zp.apply(self.ax, base_scale=1.3)

        # --- Тулбар ---
        self.toolbarframe.destroy()
        self.toolbarframe = tk.Frame()
        self.toolbarframe.pack(expand=1, fill='both')

        # self.toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2Tk(self.canvas, self.toolbarframe)
        # self.toolbar.update()

        self.label.configure(text=filename)

        # self.ax.text(737573.3281182902, 20, 'TEST')
        # self.scatter = self.ax.scatter([737573.3281182902], [20])
        self.scatter1 = None
        self.scatter2 = None
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)


    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir=curdir, title="Select A File",
                                                   filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        self.graph_draw(self.filename)


if __name__ == '__main__':
    app = MainTk()
    app.mainloop()
