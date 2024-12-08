#!/usr/bin/env python3

"""
AWS Resources.
"""

from dataclasses import dataclass

@dataclass
class AMI:
    # Amazon_Linux_2  = 'ami-0c02fb55956c7d316' bad
    Amazon_Linux_2  = 'ami-0f0f9d42fd1e4ac96'
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
    bch_allows_vnc   = 'sg-0f9a9fb1233e294aa'
