#!/usr/bin/env python3
from typing_extensions import Annotated

import typer

from bh_aws.util import run
from bh_aws.constants import PROFILE, PEM
from bh_aws import Session

from .cmd_tmp import app as tmp_app

app = typer.Typer()
app.add_typer(tmp_app, name="tmp")


@app.callback()
def dummy():
    """Manage ec2 instances
    """

@app.command()
def list( profile: str='showme'):
    """list all aws ec2 instances with state.
    """
    s=Session(profile)
    for inst in s.instances():
        print( inst )

@app.command()
def stop( name: str, profile: str='showme'):
    """Stop the ec2 instance with the given name.
    """
    inst=Session(profile).inst4name(name)
    print( f"stopping: {inst}" )
    if inst:
        inst.i.stop()

@app.command()
def start( name: str, profile: str='showme'):
    """Start the ec2 instance with the given name.
    """
    inst=Session(profile).inst4name(name)
    print( f"starting: {inst}" )
    if inst:
        inst.i.start()

@app.command()
def ssh(
    name: Annotated[ str, typer.Option( help="Name of the host.") ]
    , profile: str=PROFILE
    , user: str='ubuntu'
    , i: Annotated[ str, typer.Option( help="Identity file.") ]=PEM
    , dry: bool=False
    ):
    """Create an ssh connection to a running ec2 instance.
    """
    inst = Session(profile).inst4name(name)
    if inst is None:
        print( 'host not found' )
        return
    ip = inst.i.public_ip_address
    if ip is None:
        print( 'host not running' )
        return
    line= f"ssh -i {i} {user}@{ip}"
    run(line, dry=dry)

