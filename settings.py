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

        self._js = None
        self.load()

    def load(self):
        with open(self.filepath, 'r') as f:
            self._js = json.load(f)

    def save(self):
        with open(self.filepath, 'rw') as fw:
            json.dump(self._js, fw, indent=4, ensure_ascii=False)

    def __getitem__(self, item):
        if item in self._js:
            return self._js[item]
        else:
            return None
            # raise KeyError()

    def __setitem__(self, key, value):
        self._js[item] = value
        # if item in self._js:
        #    self._js[item] = value
        # else:
        #    raise KeyError()


if __name__ == '__main__':
    settings = Settings()
