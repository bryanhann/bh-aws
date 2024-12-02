#!/usr/bin/env python3
import boto3

def boto_dikt4tags(tags):
    acc={}
    if tags is None:
        return acc
    for tag in tags:
        acc[tag['Key']] = tag['Value']
    return acc

class BotoInstance:
    def __init__(self,inst):
        self.i = inst
    def addr(self):
        if self.state() == 'running':
            return self.i.public_ip_address
        else:
            return ''
    def tags(self):
        return boto_dikt4tags(self.i.tags)
    def name(s):
        tags = s.tags()
        if tags == None:
            return 'NONE'
        return s.tags().get('Name')
    def state(s):
        return s.i.state['Name']
    def __repr__(s):
        return f"<{s.name()} {s.i.state['Name']}> ip[{s.i.public_ip_address}]"
    def root_login(s):
        """Return root login name mased on instance name
        """
        machine_code = s.name().split('-')[-1]
        if machine_code in 'ubuntu x'.split():
            return 'ubuntu'
        if machine_code in 'amazon x'.split():
            return 'ec2-user'
        return 'guest'

class Session:
    def instances(self):
        for inst in self.r.instances.all():
            yield BotoInstance(inst)
    def __init__(self, profile):
        self.s = boto3.Session(profile_name=profile)
        self.r = self.s.resource('ec2')
        self.c = self.s.client('ec2')
    def tmp_instances(self):
        for inst in self.instances():
            if inst.name().startswith('tmp-'):
                yield inst
    def running_instances(self):
        for inst in self.instances():
            if inst.state() == 'running':
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

