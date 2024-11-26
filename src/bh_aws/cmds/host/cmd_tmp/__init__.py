#!/usr/bin/env python3
from typing_extensions import Annotated
from pprint import pprint

import boto3

import typer

from bh_aws.constants import PROFILE
from bh_aws import Session

from .specs import SPECS

app = typer.Typer()

@app.callback()
def dummy():
    """Manage temporary ec2 instances
    """

@app.command()
def stop(
    profile: str=PROFILE
    ):
    """Stop all temporary [tmp-*] ec2 instances
    """
    s=Session(profile)
    for inst in s.tmp_instances():
        print(f"stopping: {inst}")
        inst.i.stop()

@app.command()
def terminate(
    profile: str=PROFILE
    ):
    """Terminate all temporary [tmp-*] instances
    """
    s=Session(profile)
    for inst in s.tmp_instances():
        print(f"terminating: {inst}")
        inst.i.terminate()

@app.command()
def launch(
    spec: str=''
    ):
    if not spec in SPECS:
        aa = '|'.join(SPECS.keys())
        print( f'--specs {aa}' )
        return
    template=SPECS[spec]
    pprint(template.as_dict())
    s=Session(template.profile)
    s.c.run_instances(**template.as_dict())

