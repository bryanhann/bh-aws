#!/usr/bin/env python3
from typing_extensions import Annotated

import typer

from bh_aws.util import run
from bh_aws.constants import PROFILE
#from bh_aws import allinstances
from bh_aws import Session
from .launcher import Launcher

app = typer.Typer()

#def tmps(): return [x for x in allinstances() if x.name().startswith('tmp-')]
#def ids4instances(xS): return ' '.join( [ x.id() for x in xS ] )

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
    profile: str=PROFILE
    , userdata: str='ubuntu'
    , template: str='2'
    , dry: bool=False
    ):
    """Launch a new temporary ec2 instance.
    """
    try:
        launcher=Launcher(
            profile=profile
            , dry=dry
            , userdata=userdata
            , template=template
        )
    except Launcher.EXC_userdata:
        print( f'failed: [--userdata {userdata}]' )
        exit()
    run(launcher._cmdline())

