#!/usr/bin/env python3

import typer

from .cmds.key import app as key
from .cmds.host import app as host

app = typer.Typer()

app.add_typer(key, name="key")
app.add_typer(host, name="host")
def main() -> None:
    app()

