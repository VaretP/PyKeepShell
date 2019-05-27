# PyKeepShell
[![buddy pipeline](https://app.buddy.works/paulvaret/pykeepshell/pipelines/pipeline/189735/badge.svg?token=b8c8537e7b306ecabd2e06460e5dc7794e3ffe59903108c44232f58c0cc17c26 "buddy pipeline")](https://app.buddy.works/paulvaret/pykeepshell/pipelines/pipeline/189735)

## Installation
```
$ git clone https://github.com/VaretP/PyKeepShell
$ cd PyKeepShell
$ sudo python setup.py install
$ sudo pip install .
```
## Usage

Type `pykeep` anywhere in your shell.

#### Commands :

- `list`: list all files in pykeep
- `check ...args`: check if any files can be updated
- `add path alias`: add path as alias into pykeep
- `pull args...`: replace files in pykeep from their path
- `update ..args`: apply changes on files that can be updated
- `edit args...`: start your **$EDITOR** (*default vim*) on args
- `git ...args`: execute git commands in pykeep
- `help`: show help
- `exit`: close pykeep
