#!/usr/bin/env python3

from dataclasses import dataclass

from .util import userdata, tags4name
from .aws import AMI, SUBNET, SG
from .abc import Showme_ABC

@dataclass
class Amazon(Showme_ABC):
    UserData             = userdata('yum.sh')
    ImageId              = AMI.Amazon_Linux_2
    SecurityGroupIds     = [SG.default]
    TagSpecifications    = tags4name('amazon')

@dataclass
class Ubuntu(Showme_ABC):
    UserData             = userdata('apt.sh')
    ImageId              = AMI.UbuntuA
    SecurityGroupIds     = [SG.default]
    TagSpecifications    = tags4name('Ubuntu')

@dataclass
class Suse(Showme_ABC):
    UserData             = userdata('suse.sh')
    ImageId              = AMI.Suse
    SecurityGroupIds     = [SG.default]
    TagSpecifications    = tags4name('Suse')
    SubnetId             = SUBNET.default

SPECS={}
SPECS['ubuntu'] = Ubuntu()
SPECS['suse'] = Suse()
SPECS['amazon'] = Amazon()
