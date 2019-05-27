from pykeep.shell import *
from pykeep.config import *

def main():
    config = Config('~/.pykeep')
    sh = Shell('Pykeep > ', config)
    sh.loop()

if __name__ == '__main__':
    main()
