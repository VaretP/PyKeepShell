import os.path
import filecmp


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
        
    def readPkConf(self) -> dict:
        d = {}
        with open(self.pkConf, 'r') as pkConf:
            d = dict((k, v) for k, v in (line.strip().split(' ')
                     for line in pkConf.readlines()))
        return d

    def getNeededUpdates(self) -> dict:
        needUpdate = {}
        for alias, path in self.readPkConf().items():
            if not filecmp.cmp(path, f'{self.path}/{alias}'):
                needUpdate[alias] = path
        return needUpdate
