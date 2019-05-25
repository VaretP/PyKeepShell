import readline
import subprocess
from config import Config


class Shell():

    def __init__(self, prompt: str, conf: Config):
        self.prompt = prompt
        self.conf = conf
        self.commands = {
                'ls': self.ls,
        }
        readline.parse_and_bind('tab: complete')

    def ls(self, args: list) -> None:
        subprocess.run(['ls', '--color=auto', self.conf.path])

    #@staticmethod
    def complete(self, text, state):
        results = [cmd for cmd in self.commands.keys()  if cmd.startswith(text)]
        return results[state]

    def loop(self) -> None:
        readline.set_completer(self.complete)
        while 1:
            try:
                line = input(self.prompt).split(' ')
                if line[0] == 'exit':
                    break
                try:
                    self.commands[line[0]](line[1:])
                except KeyError:
                    print(f'pykeep: command not found: {line[0]}')
            except EOFError:
                print()
                break
