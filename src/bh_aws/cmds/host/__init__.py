#!/usr/bin/env python3

import typer

from bh_aws.util import stderr, cli, run
from bh_aws.constants import PROFILE, REFRESH

from .aws import allinstances, inst4name, ip4name
from .specs import Ubuntu, Suse

SPECS={}
SPECS['ubuntu'] = Ubuntu
SPECS['suse'] = Suse

app = typer.Typer()

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
    """Stop the ec2 instance with the given name.
    """
    inst=inst4name(name)
    if not inst: return
    line = f"aws ec2 --profile {profile} stop-instances --instance-ids {inst.id()}"
    run(line, dry=dry)

@app.command()
def ip(name):
    """Print the public ip address of a running ec2 instance.
    """
    print( ip4name(name))

@app.command()
def ssh(name: str, dry: bool=False, profile: str=PROFILE, user: str='ubuntu'):
    """Create an ssh connection to a running ec2 instance.
    """
    host=ip4name(name)
    if not host:
        print( 'host is not running' )
        return
    pem=f"~/.ssh/{name}.pem"
    line= f"ssh -i {pem} {user}@{host}"
    run(line, dry=dry)

@app.command()
def dev__launch(keyname: str, dry: bool=False, profile: str=PROFILE, spec: str='ubuntu'):
    """Under development: launch a new ec2 intance."""
    spec = SPECS[spec]
    print( dir(spec) )
    line = f"""
    aws ec2 run-instances
    --profile showme
    --image-id {spec.image_id}
    --instance-type {spec.instance_type}
    --subnet-id {spec.subnet_id}
    --security-group-ids {spec.security_group_ids}
    --count {spec.count}
    --key-name {keyname}
    """
    run(line)

