import os
import json

class Settings():
    def __init__(self, filepath=None):
        curdir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        if not filepath:
            self.filepath = os.path.join(curdir, 'settings.cfg')
        elif not os.path.exists(filepath):
            self.filepath = os.path.join(curdir, filepath)
        else:
            self.filepath = filepath

        if not os.path.exists(self.filepath):
            raise Exception('Не найдены настройки {}'.format(self.filepath))
        
        with open(self.filepath, 'r') as f:
            js = json.load(f)
       
            self.default_csv = js.get('default_csv', '')
            self.window_width = js.get('window_width', 0)
            self.window_height = js.get('window_height', 0)
            self.speed_color = js.get('speed_color', 'green')
            self.power_color = js.get('power_color', 'red')
            self.text_near_cursor = True if js.get('text_near_cursor', 'on')=='on' else False
       
        
        
if __name__ == '__main__':
    settings = Settings()