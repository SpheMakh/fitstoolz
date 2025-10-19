import click

from fitstoolz.scripts import stack


@click.group()
def cli():
    pass


cli.add_command(stack.runit)
