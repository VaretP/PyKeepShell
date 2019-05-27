from pykeep.shell import *
from pykeep.config import *

def main():
    config = Config('~/.pykeep')
    sh = Shell('\033[94mPykeep >\033[0m ', config)
    sh.loop()

if __name__ == '__main__':
    main()
