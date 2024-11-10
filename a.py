#!/usr/bin/env python3
import tomllib
import time
from pprint import pprint
from pathlib import Path
NOTE = " # bh.bump: this line must be first."
TOML = Path('./pyproject.toml')
for ii in range(100, 199):
    SAVE = Path(f'./pyproject.toml.save.{ii}')
    if not SAVE.exists():
        break




def main():
    def find(lines,target):
        lines = lines[:]
        acc = []
        while lines:
            acc.append(lines.pop(0))
            if acc[-1].startswith( target ):
                return acc, lines

    note = ' # version this must come first!'
    old =  TOML.read_text()
    tail = old.split('\n')
    aa , tail = find(tail, '[project]')
    bb , tail = find(tail, 'version')
    aa.append(bb.pop(-1).split('#')[0].strip() + note)
    new = '\n'.join(aa + bb + tail)
    if new == old:
        print( 'no change' )
        exit()
    SAVE.write_text( old )
    TOML.write_text( new )
if __name__ == '__main__':
    main()
