#!/usr/bin/env python3

import boto3
from rich.text import Text


class BotoInstance:
    def __init__(self,inst):
        self._it = inst
        self.i = inst # legacy

    def root_login(s):
        """Return root login name mased on instance name
        """
        name  = s.name().lower()
        if 'ubuntu' in name: return 'ubuntu'
        if 'amazon' in name: return 'ec2-user'
        if True:             return 'guest'

    def ip(s):
        """The public_ip_address of the instance, or empty string
        """
        return s._it.public_ip_address or ''

    def id(s):
        """The instance_id ip address of the instance
        """
        return s._it.instance_id

    def rich(s):
        """A rich text version of self.__repr__
        """
        if   s.state() == 'running' : style = 'bold black'
        elif s.state() == 'stopped' : style = 'black'
        else                        : style = 'magenta'
        text = Text()
        text.append(f'{s}', style=style)
        return text


    def name(s):
        """The instance name from tags, default 'NONE'
        """
        try:
            return s._tags()['Name']
        except:
            return 'NONE'

    def state(s):
        """The state of the instance as a string: 'running|stopped|terminated' etc.
        """
        return s._it.state['Name']

    def __repr__(s):
        acc=[]
        acc.append(s.__class__.__name__)
        acc.append(s.id()[:6])
        acc.append(s.name())
        acc.append(s.ip())
        acc.append(s.state())
        line = '|'.join(acc)
        return f'[{line}]'

    def _tags(self):
        def boto_dikt4tags(tags):
            acc={}
            if tags is None:
                return acc
            for tag in tags:
                acc[tag['Key']] = tag['Value']
            return acc
        return boto_dikt4tags(self._it.tags)

class Session:
    def __init__(self, profile):
        self.s = boto3.Session(profile_name=profile)
        self.r = self.s.resource('ec2')
        self.c = self.s.client('ec2')

    def instances(self):
        """Yield all instances
        """
        for inst in self.r.instances.all():
            yield BotoInstance(inst)

    def tmp_instances(self):
        """Yield all temporary instances
        """
        for inst in self.instances():
            if inst.name().startswith('tmp-'):
                yield inst

    def running_instances(self):
        """Yield all running instances
        """
        for inst in self.instances():
            if inst.state() == 'running':
                yield inst

    def inst4name(self, name):
        for inst in self.instances():
            if inst.name() == name:
                return inst

