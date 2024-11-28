#!/usr/bin/env python3

from dataclasses import dataclass

from .util import userdata, tags4name
from .aws import AMI, SUBNET, SG
from .abc import Showme_ABC

@dataclass
class Ubuntu(Showme_ABC):
    UserData             = userdata('ubuntu.sh')
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
