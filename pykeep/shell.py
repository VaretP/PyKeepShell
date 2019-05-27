import readline
import subprocess
import os
import shutil
from pykeep.config import Config


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class Shell():

    def __init__(self, prompt: str, conf: Config):
        self.prompt = prompt
        self.conf = conf
        self.commands = {
                'list': self.list,
                'add': self.add,
                'edit': self.edit,
                'pull': self.pull,
                'check': self.check,
                'update': self.update,
        }
        readline.parse_and_bind('tab: complete')

    def list(self, args: list) -> None:
        possibleFiles = self.conf.readPkConf().keys()
        needUpdate = self.conf.getNeededUpdates().keys()
        out = ''
        for f in os.listdir(self.conf.path):
            if f not in possibleFiles:
                out += f'  {colors.FAIL}{f}{colors.END}'
            elif f in needUpdate:
                out += f'  {colors.WARNING}{f}{colors.END}'
            else:
                out += f'  {f}'
        print(out)

    def add(self, args: list) -> None:
        if len(args) != 2:
            print(f'{colors.WARNING}add: usage: add "path" "alias"{colors.END}')
            return
        path = os.path.expanduser(args[0])
        try:
            shutil.copyfile(path, f'{self.conf.path}/{args[1]}')
        except FileNotFoundError:
            print(f'{colors.FAIL}no such file or directory:'
                  f'{args[0]}{colors.END}')
            return
        with open(self.conf.pkConf, 'a') as pkConf:
            pkConf.write(f'{args[1]} {path}\n')

    def edit(self, args: list) -> None:
        if len(args) == 0:
            print(f'{colors.WARNING}edit: usage: edit file{colors.END}')
            return
        possibleFiles = self.conf.readPkConf().keys()
        editor = os.environ.get('EDITOR', 'vim')
        files = []
        for alias in args:
            if alias not in possibleFiles:
                print(f'{colors.FAIL}no such file "{alias}"{colors.END}')
            else:
                files.append(f'{self.conf.path}/{alias}')
        subprocess.run([editor] + files)

    def check(self, args: list) -> None:
        needUpdate = self.conf.getNeededUpdates().keys()
        if len(needUpdate) != 0:
            for alias in needUpdate:
                print(f'"{alias}" can be updated.')
        else:
            print(f'{colors.GREEN}Everything is up to date{colors.END}')

    def update(self, args: list) -> None:
        needUpdate = self.conf.getNeededUpdates()
        if len(args) != 0:
            possibleFiles = self.conf.readPkConf().keys()
            for alias in args:
                if alias not in possibleFiles:
                    print(f'{colors.FAIL}Unknown file: {alias}{colors.END}')
                elif alias in needUpdate.keys():
                    path = needUpdate[alias]
                    shutil.copyfile(f'{self.conf.path}/{alias}', path)
                    print(f'{colors.GREEN}Updated {alias}.{colors.END}')
                else:
                    print(f'{colors.WARNING}{alias} is already up to date'
                          f'{colors.END}')
        else:
            if len(needUpdate) == 0:
                print(f'{colors.GREEN}Already up to date{colors.END}')
            else:
                for alias, path in needUpdate.items():
                    shutil.copyfile(f'{self.conf.path}/{alias}', path)
                    print(f'{colors.GREEN}Updated {alias}.{colors.END}')

    def pull(self, args: list) -> None:
        needUpdate = self.conf.getNeededUpdates()
        if len(args) != 0:
            possibleFiles = self.conf.readPkConf().keys()
            for alias in args:
                if alias not in possibleFiles:
                    print(f'{colors.FAIL}Unknown file: {alias}{colors.END}')
                elif alias in needUpdate.keys():
                    path = needUpdate[alias]
                    shutil.copyfile(path, f'{self.conf.path}/{alias}')
                    print(f'{colors.GREEN}Pulled {alias}.{colors.END}')
                else:
                    print(f'{colors.WARNING}{alias} is already up to date'
                          f'{colors.END}')
        else:
            print(f'{colors.WARNING}pull: usage: pull "file" ...{colors.END}')

    def complete(self, text: str, state: int) -> str:
        if text == '':
            return None
        results = [cmd for cmd in self.commands.keys()
                   if cmd.startswith(text)]
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
                    print(f'{colors.FAIL}Command not found: {line[0]}'
                          f'{colors.END}')
            except EOFError and KeyboardInterrupt:
                print()
                break
