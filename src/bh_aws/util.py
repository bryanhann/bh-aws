import sys
import subprocess
import string

from rich.console import Console
from colorama import Fore, Back, Style

rprint = Console().print

def stderr(txt):
    sys.stderr.write(str(txt) + '\n')
    sys.stderr.flush()

def bold(text):
    return Style.BRIGHT + Fore.RED + text + Style.RESET_ALL

def cli(line):
    stderr( '\nExecute the following:' )
    stderr(f'    {bold(line)}')

def runc(line,dry=False):
    return run(line, dry, capture=True)

def run(line, dry=False, capture=False):
    stderr( '\nRunning:')
    stderr(f'    {bold(line)}')
    if dry: return
    return subprocess.run(
        line.split(),
        capture_output=capture,
        text=True
    )

def prompt_yes(msg=''):
    print(msg)
    a = (input( 'type YES to proceed: ' ).lower() + 'x')[0]
    if a =='y':
        return True
    else:
        print( 'aborting' )
        return False

def dmenu(dikt):
    choice = menu(dikt.keys())
    if choice:
        return dikt[choice]

def menu(o):
    def rich(x):
        if hasattr(x,'rich'):
            return x.rich()
        else:
            return x
    o = dict( zip(string.ascii_lowercase, o ) )
    if not o:
        print('No options.')
        return None
    while True:
        for k,v in o.items():
            rprint(f"{k})", rich(v))
        choice = input( 'enter option: ' ).strip().lower()[:1]
        if choice in o.keys():
            return o[choice]
        if not choice:
            return None

