import readline
import subprocess
from config import *


class Shell():

    options = ['ls', 'exit']
    
    def __init__(self, prompt: str, conf: Config):
        self.prompt = prompt
        self.conf = conf
        readline.parse_and_bind('tab: complete')

    def ls(self) -> None:
        subprocess.run(['ls', '--color=auto', self.conf.path])


    @staticmethod
    def complete(text, state):
        results = [cmd for cmd in Shell.options if cmd.startswith(text)]
        return results[state]

    def loop(self) -> None:
        commands = {
                'ls': self.ls,
        }
        readline.set_completer(Shell.complete)
        while 1:
            try:
                line = input(self.prompt)
                if line == 'exit':
                    break
                try:
                    commands[line]()
                except:
                    print(f'pykeep: command not found: {line}')
            except EOFError:
                print()
                return
