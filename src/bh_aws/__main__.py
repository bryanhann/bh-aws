#!/usr/bin/env python3

import typer

from .aws import allinstances, inst4name, ip4name
from .util import stderr, cli, run
from .constants import PROFILE, REFRESH

app = typer.Typer()

@app.command()
def listall():
    """list all aws ec2 instances with state

    They must have a tag naming them.
    """
    for inst in allinstances():
        print(inst)


@app.command()
def start(name: str, dry: bool=False, profile: str=PROFILE):
    """Start the ec2 instance with the given name.
    """
    inst=inst4name(name)
    if not inst:
        return
    line = f"aws ec2 --profile {profile} start-instances --instance-ids {inst.id()}"
    run(line, dry=dry)

@app.command()
def stop(name: str, dry: bool=False, profile: str=PROFILE):
    inst=inst4name(name)
    if not inst: return
    line = f"aws ec2 --profile {profile} stop-instances --instance-ids {inst.id()}"
    run(line, dry=dry)

@app.command()
def ip(name):
    """Echo the public ip address of ec2 instance to STDOUT
    """
    print( ip4name(name))


@app.command()
def ssh(name: str, dry: bool=False, profile: str=PROFILE, user: str='ubuntu'):
    host=ip4name(name)
    if not host:
        print( 'host is not running' )
        return
    pem=f"~/.ssh/{name}.pem"
    line= f"ssh -i {pem} {user}@{host}"
    run(line, dry=dry)


def main() -> None:
    """bh-aws-cli."""
    app()


