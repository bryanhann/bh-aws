#!/usr/bin/env python3

import string
from dataclasses import dataclass

from .util import userdata

class Template_ABC:
    def as_dict(self):
        acc = {}
        for name in dir(self):
            if name[0] in string.ascii_uppercase:
                acc[name] = getattr(self,name)
        return acc

@dataclass
class Showme_ABC(Template_ABC):
    profile              = 'showme'
    KeyName              = "aws.showme"
    InstanceType         = 't2.micro'
    MaxCount             = 1
    MinCount             = 1
    UserData             = userdata('empty.sh')

