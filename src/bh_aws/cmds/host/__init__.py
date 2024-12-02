#!/usr/bin/env python3
from pprint import pprint
import typing_extensions

import typer

from bh_aws.util import run
from bh_aws.util import menu
from bh_aws.constants import PROFILE, PEM
from bh_aws import Session

from .cmd_tmp import app as tmp_app

AA = typing_extensions.Annotated
OO = typer.Option

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
    profile: AA[ str, OO(help="AWS cli profile") ] = PROFILE
    , login: AA[ str, OO(help="Login name")      ] = ''
    , pem:   AA[ str, OO(help="Name of identity file")   ] = PEM
    , dry:   AA[ bool, OO(help="Dry run")        ] = False
    ):
    """Create an ssh connection to a running ec2 instance.
    """
    inst = menu(Session(profile).running_instances())
    if inst is None:
        return
    login = login or inst.root_login()
    ip = inst.addr()
    pem = f'~/.ssh/{pem}'
    line= f"ssh -i {pem} {login}@{ip}"
    run(line, dry=dry)


