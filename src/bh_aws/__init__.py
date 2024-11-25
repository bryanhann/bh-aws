#!/usr/bin/env python3
import boto3

def boto_dikt4tags(tags):
    acc={}
    for tag in tags:
        acc[tag['Key']] = tag['Value']
    return acc

class BotoInstance:
    def __init__(self,inst):
        self.i = inst
    def tags(self):
        return boto_dikt4tags(self.i.tags)
    def name(s):
        return s.tags().get('Name')
    def __repr__(s):
        return f"<{s.name()} {s.i.state['Name']}> ip[{s.i.public_ip_address}]"

class Session:
    def instances(self):
        for inst in self.r.instances.all():
            yield BotoInstance(inst)
    def __init__(self, profile):
        self.s = boto3.Session(profile_name=profile)
        self.r = self.s.resource('ec2')
    def tmp_instances(self):
        for inst in self.instances():
            if inst.name().startswith('tmp-'):
                yield inst
    def inst4name(self, name):
        for inst in self.instances():
            if inst.name() == name:
                return inst

import json
import subprocess
import pathlib
import sys

from .util import stderr, bold
from .instance import Instance
from .stuff import allinstances
from .stuff import inst4name
from .stuff import allnames
from .stuff import id4name
from .stuff import ip4name
from .stuff import tmpname
from .stuff import names

