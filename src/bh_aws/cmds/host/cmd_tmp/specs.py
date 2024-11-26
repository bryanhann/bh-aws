#!/usr/bin/env python3
import random
from dataclasses import dataclass
import string

def tmpname(name):
    nnn = str(random.randrange(1000,1999))[1:]
    return f'tmp-{nnn}-{name}' #'-{random.randrange(1000)}'

def tags4name(name):
    return  tags4dict( { 'Name' : tmpname(name) } )

def tags4dict(d):
    acc=[]
    for key,value in d.items():
        acc.append( {'Key': key, 'Value': value } )
    return [ { 'ResourceType': 'instance', 'Tags': acc } ]

@dataclass
class AMI:
    Amazon_Linux_2  = 'ami-0c02fb55956c7d316'
    Ubuntu_other    = 'ami-00498a47f0a5d4232'
    Suse            = 'ami-0226a08ab7f8c5d03'
    UbuntuA         = 'ami-048ddca51ab3229ab' # Ubuntu-A
    UbuntuB         = 'ami-0eb9fdcf0d07bd5ef'

@dataclass
class SUBNET:
    aaa          = 'subnet-0984555689f5894d8'
    bbb          = 'subnet-0c7a12f30319923aa'
    default      = 'subnet-051fcbe4e4f4cc521' # Ubuntu-A , Suse

@dataclass
class SG:
    aaa              = 'sg-01304974040835e2f'
    default          = 'sg-0b9a4ef40ee78a621' # Ubuntu-A

USER_DATA = '''#!/bin/bash
yum update
'''

@dataclass
class ABC:
    def as_dict(self):
        acc = {}
        for name in dir(self):
            if name[0] in string.ascii_uppercase:
                acc[name] = getattr(self,name)
        return acc

@dataclass
class Showme(ABC):
    profile              = 'showme'
    KeyName              = "aws.showme"
    InstanceType         = 't2.micro'
    MaxCount             = 1
    MinCount             = 1


@dataclass
class Ubuntu(Showme):
    ImageId              = AMI.UbuntuA
    SecurityGroupIds     = [SG.default]
    UserData             = USER_DATA
    TagSpecifications    = tags4name('Ubuntu')

@dataclass
class Suse(Showme):
    ImageId              = AMI.Suse
    SecurityGroupIds     = [SG.default]
    TagSpecifications    = tags4name('Suse')
    SubnetId             = SUBNET.default

SPECS={}
SPECS['Ubuntu'] = Ubuntu()
SPECS['Suse'] = Suse()
