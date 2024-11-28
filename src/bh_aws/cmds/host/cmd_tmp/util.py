#!/usr/bin/env python3
import random
from pathlib import Path

USERDATA=Path(__file__).parent/'userdata.d'

class SpecsException(BaseException):
    pass

def userdata(name):
    pth=USERDATA/name
    if not pth.exists():
        raise SpecsException(f'\n\tmissing userdata: {pth}')
    assert pth.exists()
    return pth.read_text()

def tmpname(name):
    nnn = str(random.randrange(1000,1999))[1:]
    return f'tmp-{nnn}-{name}' #'-{random.randrange(1000)}'

def tags4name(name):
    return  tags4dict( { 'Name' : tmpname(name) } )

def tags4dict(d):
    acc=[]
    for key,value in d.items():
        acc.append( {'Key': key, 'Value': value } )

