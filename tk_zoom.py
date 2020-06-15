class ZoomPan:
    """ Класс параномирования и зуммирования графика для matplotlib 
        Также реагирует на Esc для выхода из программы
        Пример использования:
        fig, ax = matplotlib.pyplot.subplots()
        zp = ZoomPan()
        zp.apply(ax, base_scale=1.3)
    """ 
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def apply(self, ax, base_scale = 1.3):
        self.zoom_factory(ax, base_scale)
        self.pan_factory(ax)
        self.key_factory(ax)
        self.mouse_factory(ax)
        self.mouse_move_factory(ax)
        
    def on_key_press(self, event):
        # Выход из программы
        if event.key == 'escape':
            #exit()
            pass
        #print(event)
    
    def key_factory(self, ax):
        fig = ax.get_figure()
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
    
        
    def mouse_factory(self, ax):
        def on_mouse_release(event):
            if event.button==2:
                #print('MIDDLE')
                print(ax.get_xlim(), ax.get_ylim())
            #print(event)
        fig = ax.get_figure()
        fig.canvas.mpl_connect('button_release_event', on_mouse_release)
        
    def mouse_move_factory(self, ax):
        def on_mouse_move(event):
            pass
            #print(event)
        fig = ax.get_figure()
        fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
    
    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print( event.button)
            
            scalex = True
            scaley = False
            
            if event.key == 'control':
                scalex = True
                scaley = True
            elif event.key == 'alt':
                scalex = False
                scaley = True
            
            if scalex:
                new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
                relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
                ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])

            if scaley:
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
                rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
                ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])


            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            
            panx = True
            pany = False
            if event.key == 'control':
                panx = True
                pany = True
            elif event.key == 'alt':
                panx = False
                pany = True
                
            if panx:
                dx = event.xdata - self.xpress
                self.cur_xlim -= dx
                ax.set_xlim(self.cur_xlim)
            if pany:
                dy = event.ydata - self.ypress
                self.cur_ylim -= dy
                ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion
               