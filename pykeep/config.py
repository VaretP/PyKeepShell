import os.path

class Config():

    def __init__(self, path: str):
        self.path = os.path.expanduser(path)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print('Created directory ' + path)
        elif not os.path.isdir(self.path):
            raise ValueError('Config path should be a directory')
        self.pkConf = os.path.expanduser('~/.pkconf')
        open(self.pkConf, 'a').close()
