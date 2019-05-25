from shell import *
from config import *

if __name__ == '__main__':
    config = Config('~/.pykeep')
    sh = Shell("> ", config)
    sh.loop()
