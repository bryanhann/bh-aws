import sys
import subprocess

from colorama import Fore, Back, Style

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

