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
    return [{'ResourceType': 'instance', 'Tags': acc}]

def inject4dikt4name(dikt,name):
    """Override the 'name' tag in template dictionary
    """
    def isnumber(x):
        try: int('1' + x) + 2
        except: return False
        return True
    for ii,tspec in enumerate(dikt['TagSpecifications']):
        for jj,tag in enumerate(tspec['Tags']):
            if tag['Key'] == 'Name':
                old = tag['Value']
                old = old.split( '-' )
                old and old[0] == 'tmp' and old.pop(0)
                old and isnumber(old[0]) and old.pop(0)
                old = '-'.join(old)
                tag['Value'] = f'{name}-{old}'

