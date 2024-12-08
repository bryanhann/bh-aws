#!/usr/bin/env python3
from pprint import pprint
import typing_extensions

import typer

from bh_aws import Session
from bh_aws.util import run, menu, dmenu, prompt_yes
from bh_aws.constants import PROFILE, PEM
from bh_aws.launch import SPECS
from bh_aws.launch.util import inject4dikt4name

AA = typing_extensions.Annotated
OO = typer.Option
app = typer.Typer()


@app.callback()
def dummy():
    """Manage ec2 instances
    """


@app.command()
def list( profile: str='showme'):
    """List ec2 instances.
    """
    for inst in Session(profile).instances():
        print( inst )


@app.command()
def terminate( profile: str='showme'):
    """Terminate ec2 instance from menu.
    """
    inst = menu(Session(profile).instances())
    if not inst:
        return
    if prompt_yes(f'terminating {inst}' ):
        inst.i.terminate()


@app.command()
def stop( profile: str='showme'):
    """Stop ec2 instance from menu.
    """
    inst = menu(Session(profile).instances())
    if inst:
        inst.i.stop()


@app.command()
def start( profile: str='showme'):
    """Start ec2 instance from menu.
    """
    inst = menu(Session(profile).instances())
    if inst:
        inst.i.start()


@app.command()
def ssh(
    profile: AA[ str, OO(help="AWS cli profile") ] = PROFILE
    , login: AA[ str, OO(help="Login name")      ] = ''
    , pem:   AA[ str, OO(help="Name of identity file")   ] = PEM
    , dry:   AA[ bool, OO(help="Dry run")        ] = False
    ):
    """SSH to instance from menu.
    """
    inst = menu(Session(profile).running_instances())
    if inst is None:
        return
    login = login or inst.root_login()
    ip = inst.addr()
    pem = f'~/.ssh/{pem}'
    line= f"ssh -i {pem} {login}@{ip}"
    run(line, dry=dry)


@app.command()
def launch(
    dry: bool=False
    , name: str = ''
    , profile: str = PROFILE
    ):
    """Launch an ec2 instance.
    """
    template = dmenu(SPECS)
    if template is None:
        return
    dikt = template.as_dict()
    print('-'*60)
    pprint(dikt)
    if name:
        inject4dikt4name(dikt,name)
        print('-'*60)
        pprint(dikt)
    if dry:
        print('dry run')
    else:
        s=Session(profile)
        s.c.run_instances(**template.as_dict())


@app.command()
def cleanup(
    profile: str=PROFILE
    ):
    """Terminate all temporary [tmp-*] instances
    """
    s=Session(profile)
    for inst in s.tmp_instances():
        print(f"terminating: {inst}")
        inst.i.terminate()

