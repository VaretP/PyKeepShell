import readline
import subprocess
import os
import shutil
import filecmp
from config import Config


class Shell():

    def __init__(self, prompt: str, conf: Config):
        self.prompt = prompt
        self.conf = conf
        self.commands = {
                'ls': self.ls,
                'add': self.add,
                'edit': self.edit,
                'check': self.check,
                'update': self.update,
                'pull': self.pull,
        }
        readline.parse_and_bind('tab: complete')

    def readPkConf(self) -> dict:
        d = {}
        with open(self.conf.pkConf, 'r') as pkConf:
            d = dict((k, v) for k, v in (line.strip().split(' ')
                     for line in pkConf.readlines()))
        return d

    def getNeededUpdates(self) -> dict:
        needUpdate = {}
        for alias, path in self.readPkConf().items():
            if not filecmp.cmp(path, f'{self.conf.path}/{alias}'):
                needUpdate[alias] = path
        return needUpdate

    def ls(self, args: list) -> None:
        subprocess.run(['ls', '--color=auto', self.conf.path])

    def add(self, args: list) -> None:
        if len(args) != 2:
            print('add: usage: add "path" "alias"')
            return
        path = os.path.expanduser(args[0])
        try:
            shutil.copyfile(path, f'{self.conf.path}/{args[1]}')
        except FileNotFoundError:
            print(f'no such file or directory: {args[0]}')
            return
        with open(self.conf.pkConf, 'a') as pkConf:
            pkConf.write(f'{args[1]} {path}\n')

    def edit(self, args: list) -> None:
        editor = os.environ.get('EDITOR', 'vim')
        subprocess.run([editor] + [f'{self.conf.path}/{alias}' for alias in args])

    def check(self, args: list) -> None:
        needUpdate = self.getNeededUpdates().keys()
        if len(needUpdate) != 0:
            for alias in needUpdate:
                print(f'"{alias}" can be updated.')
        else:
            print('Everything is up to date')

    def update(self, args: list) -> None:
        needUpdate = self.getNeededUpdates()
        if len(args) != 0:
            possibleFiles = self.readPkConf().keys()
            for alias in args:
                if alias not in possibleFiles:
                    print(f'Unknown file: {alias}')
                elif alias in needUpdate.keys():
                    path = needUpdate[alias]
                    shutil.copyfile(f'{self.conf.path}/{alias}', path)
                    print(f'Updated {alias}.')
                else:
                    print(f'{alias} is already up to date')
        else:
            if len(needUpdate) == 0:
                print('Already up to date')
            else:
                for alias, path in needUpdate.items():
                    shutil.copyfile(f'{self.conf.path}/{alias}', path)
                    print(f'Updated {alias}.')

    def pull(self, args: list) -> None:
        needUpdate = self.getNeededUpdates()
        if len(args) != 0:
            possibleFiles = self.readPkConf().keys()
            for alias in args:
                if alias not in possibleFiles:
                    print(f'Unknown file: {alias}')
                elif alias in needUpdate.keys():
                    path = needUpdate[alias]
                    shutil.copyfile(path, f'{self.conf.path}/{alias}')
                    print(f'Pulled {alias}.')
                else:
                    print(f'{alias} is already up to date')
        else:
            print(f'pull: usage: pull "file" ...')

    def complete(self, text: str, state: int) -> str:
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
                    print(f'Command not found: {line[0]}')
            except EOFError and KeyboardInterrupt:
                print()
                break
