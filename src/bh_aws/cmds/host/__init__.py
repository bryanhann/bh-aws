#!/usr/bin/env python3
from typing_extensions import Annotated

import typer

from bh_aws import allinstances, inst4name, ip4name
from bh_aws.util import run
from bh_aws.constants import PROFILE, PEM

from .cmd_tmp import app as tmp_app

app = typer.Typer()
app.add_typer(tmp_app, name="tmp")


@app.callback()
def dummy():
    """Manage ec2 instances
    """

@app.command()
def list():
    """list all aws ec2 instances with state.

    They must have a tag naming them.
    """
    for inst in allinstances():
        print(f"{inst} id=[{inst.id()}]")

@app.command()
def start(
    name: str
    , profile: str=PROFILE
    , dry: bool=False
    ):
    """Start the ec2 instance with the given name.
    """
    inst=inst4name(name)
    if not inst:
        return
    line = f"aws ec2 --profile {profile} start-instances --instance-ids {inst.id()}"
    run(line, dry=dry)


@app.command()
def stop(
    name: str
    , profile: str=PROFILE
    , dry: bool=False
    ):
    """Stop the ec2 instance with the given name.
    """
    inst=inst4name(name)
    if not inst: return
    line = f"aws ec2 --profile {profile} stop-instances --instance-ids {inst.id()}"
    run(line, dry=dry)

@app.command()
def ip(
    name: str
    ):
    """Print the public ip address of a running ec2 instance.
    """
    print( ip4name(name))

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
    host=ip4name(name)
    if not host:
        print( 'host is not running' )
        return
    line= f"ssh -i {i} {user}@{host}"
    run(line, dry=dry)
