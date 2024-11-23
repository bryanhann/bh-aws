#!/usr/bin/env python3

import typer
from bh_aws.constants import PROFILE
from bh_aws.util import run, runc

app = typer.Typer()

@app.callback()
def dummy():
    """Manage keypairs"""

@app.command()
def cleanup(
        profile: str=PROFILE
    ):
    """Delete all key-pairs whose names start with 'tmp-'
    """
    names = allkeys(profile=profile)
    names = [ x for x in names if x.startswith( 'tmp-' ) ]
    for name in names:
        print( f'cleanup {name}' )
        delete( name, profile=profile )

@app.command()
def list(
        query: str='KeyPairs[*].KeyName',
        output: str='text',
        profile: str=PROFILE
    ):
    """List all keypair names
    """
    for item in allkeys(query=query, output=output, profile=profile):
        print(item)

@app.command()
def create(
        name: str,
        query: str='KeyMaterial',
        output: str='text',
        profile: str=PROFILE
    ):
    """Create a key-pair
    """
    run( f"""
        aws ec2 create-key-pair
        --key-name {name}
        --profile {profile}
        --output {output}
        --query {query}
    """)

@app.command()
def delete(
        name: str,
        output: str='text',
        profile: str=PROFILE
    ):
    """Delete a key-pair
    """
    run( f"""
        aws ec2 delete-key-pair
        --key-name {name}
        --profile {profile}
        --output {output}
    """)

###########################################################

def allkeys(
        query: str='KeyPairs[*].KeyName',
        output: str='text',
        profile: str=PROFILE
    ):
    """Return list of all keypair names
    """
    return runc(f"""
        aws ec2 describe-key-pairs
        --profile {profile}
        --output {output}
        --query {query}
    """).stdout.split()

