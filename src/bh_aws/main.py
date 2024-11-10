#!/usr/bin/env python3

import click

from .aws import allinstances, inst4name, ip4name
from .util import stderr, cli, run
from .constants import PROFILE, REFRESH

@click.group()
@click.option('--cache/--no-cache', type=bool, default=False, help='Use cached')
def group(cache):
    """Control ec2 instances.

    First argument must be the name of the instance as per its tag.
    """
    allinstances(refresh=True)


@click.command()
def listall():
    """list all aws ec2 instances with state

    They must have a tag naming them.
    """
    for inst in allinstances():
        print(inst)


@click.command()
@click.option('--profile', default=PROFILE,
    help = 'The profile name of the aws user'
)
@click.option('--dry/--no-dry', default=False,
     help = 'Just show the command line that would be executed.')
@click.argument('name')
def start(name,dry,profile):
    """Start the ec2 instance with the given name.
    """
    inst=inst4name(name)
    if not inst:
        return
    line = f"aws ec2 --profile {profile} start-instances --instance-ids {inst.id()}"
    run(line, dry=dry)


@click.command()
@click.argument('name')
def ip(name):
    """Echo the public ip address of ec2 instance to STDOUT
    """
    print( ip4name(name))

@click.command()
@click.option('--profile', default=PROFILE)
@click.argument('name')
@click.option('--dry/--no-dry', default=False,
     help = 'Just show the command line that would be executed.')
def stop(name,dry, profile):
    inst=inst4name(name)
    if not inst: return
    line = f"aws ec2 --profile {profile} stop-instances --instance-ids {inst.id()}"
    run(line, dry=dry)

@click.command()
@click.option('--user', default='ubuntu')
@click.option('--profile', default=PROFILE)
@click.option('--dry/--no-dry', default=False,
     help = 'Just show the command line that would be executed.')
@click.argument('name')
def ssh(name,dry,profile,user):
    host=ip4name(name)
    if not host:
        print( 'host is not running' )
        return
    pem=f"~/.ssh/{name}.pem"
    line= f"ssh -i {pem} {user}@{host}"
    run(line, dry=dry)

group.add_command(ssh)
group.add_command(ip)
group.add_command(start)
group.add_command(stop)
group.add_command(listall)

@click.command()
@click.version_option()
def main() -> None:
    """bh-aws-cli."""
    group()

if __name__ == '__main__':
    main(prog_name="bh-aws-cli")

